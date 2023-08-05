import argparse
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import zipfile
from .tianhua_local import Tianhua
import os
import re
import logging
import sys

pymysql.install_as_MySQLdb()
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format=
    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class Colab(object):
    def __init__(self, root_path: str, database: str) -> None:
        self.engine = create_engine(database, encoding='utf8')
        self.root_path = root_path
        sample_info_file_path = os.path.join(root_path, '导入样本信息汇总表.xlsx')
        self.sample_info_list = pd.read_excel(sample_info_file_path).set_index(
            '原样本编号', drop=False)

        self.anno_dict = {}
        self.final_dict = {}
        self.unzip_and_parse_file_path()

    def _unzip_to_uniplace(self, filename: str, target_path: str):
        myzip = zipfile.ZipFile(filename)
        myzip.extractall(target_path)

    def unzip_and_parse_file_path(self):
        bioinfo_dir = os.path.join(self.root_path, '生信分析文件')
        bioinfo_target_dir = os.path.join(self.root_path, '生信分析文件-解压')
        anno_dir = os.path.join(self.root_path, '解读文件')
        anno_target_dir = os.path.join(self.root_path, '解读文件-解压')

        for sub in os.listdir(bioinfo_dir):
            if sub.startswith('~'):
                continue

            if sub.endswith('zip'):
                filename = os.path.join(bioinfo_dir, sub)
                self._unzip_to_uniplace(filename, bioinfo_target_dir)

        for sub in os.listdir(bioinfo_target_dir):
            if sub.startswith('~'):
                continue

            if sub.endswith('final.xlsx'):
                full_path = os.path.join(bioinfo_target_dir, sub)
                self.final_dict[re.findall(r'__(.+)_', sub)[0]] = full_path

        for sub in os.listdir(anno_dir):
            if sub.startswith('~'):
                continue

            if sub.endswith('zip'):
                filename = os.path.join(anno_dir, sub)
                self._unzip_to_uniplace(filename, anno_target_dir)

        for sub in os.listdir(anno_target_dir):
            if sub.startswith('~'):
                continue

            sub_full = os.path.join(anno_target_dir, sub)
            if os.path.isdir(sub_full):
                sample_id = re.findall(r'(^.+)_', sub)[0]
                file_full = os.path.join(sub_full, 'foronepc.xlsx')
                self.anno_dict[sample_id] = file_full

    def read_and_upload(self, update=False):
        total_sample_num = 0
        upload_sample_num = 0
        existed_sample_num = 0
        final_table_missing_sample_num = 0
        anno_table_missing_sample_num = 0

        for ind in self.sample_info_list.index:
            total_sample_num += 1
            # exist
            product_id = self.sample_info_list.loc[ind]['*产品编号']
            hospital = self.sample_info_list.loc[ind]['*送检机构']
            if self.engine.execute(
                    f"select * from th_sampleinf where product_id='{product_id}' and source_sample_id='{ind}' and inspection_unit='{hospital}'"
            ).fetchone():
                logging.warning(
                    f'sample_id {ind} with product_id{product_id} and {hospital} already exists in the database '
                )
                existed_sample_num += 1
                if update:
                    logging.info(f'updating {ind}')
                    # delete the record, then reupload
                    self.engine.execute(
                        f"delete from th_sampleinf where product_id='{product_id}' and source_sample_id='{ind}'"
                    )
                else:
                    logging.info(f'skip {ind}')
                    continue

            # incomplete files
            if not (ind in self.final_dict.keys()):
                logging.warning(f'{ind} has not corresponding final file.')
                final_table_missing_sample_num += 1
                continue

            if not (ind in self.anno_dict.keys()):
                logging.warning(f'{ind} has not corresponding anno file.')
                anno_table_missing_sample_num += 1
                continue

            # read
            mut_df = pd.read_excel(self.final_dict[ind],
                                   sheet_name='filt_variation')
            here_df = pd.read_excel(self.final_dict[ind],
                                    sheet_name='final_hereditary_tumor')
            msi_df = pd.read_excel(self.final_dict[ind], sheet_name='MSI')
            tmb_df = pd.read_excel(self.final_dict[ind], sheet_name='TMB')
            cnv_df = pd.read_excel(self.final_dict[ind],
                                   sheet_name='final.CNV')
            sv_df = pd.read_excel(self.final_dict[ind], sheet_name='filt_sv')
            cli_df = self.sample_info_list.loc[[ind]]

            anno_df = pd.read_excel(self.anno_dict[ind], sheet_name='1.3用药提示')

            th = Tianhua(cli_df, mut_df, here_df, msi_df, tmb_df, cnv_df,
                         sv_df, self.engine)
            # has_drug logic
            th.annotate(anno_df)
            # upload
            th.upload()
            upload_sample_num += 1
            logging.info(f'{ind} upload successfully.')

        summary = f"""Total sample number: {total_sample_num}
        Existed sample number: {existed_sample_num}
        Fanal table missing sample number: {final_table_missing_sample_num}
        Anno table missing sample number: {anno_table_missing_sample_num}
        Uploaded sample number: {upload_sample_num} 
        """
        logging.info(summary)


def interface():
    """
    argparse interface.

    Returns:
        tuple: () 
    """
    parser = argparse.ArgumentParser(
        description="tools for curating colab gene test data to bgi-PETA ")
    parser.add_argument("-d",
                        "--root_path",
                        type=str,
                        required=True,
                        help="root path for the product files of a colab")

    parser.add_argument(
        "-s",
        "--database",
        type=str,
        default='mysql+mysqldb://ljl:123456@172.16.208.62:3306/tianhua',
        help="database login path")

    parser.add_argument("-u",
                        "--update",
                        action='store_true',
                        default=False,
                        help="update for existing samples, skip if False")

    args = parser.parse_args()
    return args


def main():
    args = interface()
    colab = Colab(root_path=args.root_path, database=args.database)
    colab.read_and_upload(update=args.update)


if __name__ == '__main__':
    main()
