import pandas as pd
import re
import pymysql
import sqlalchemy
from .th_column_names import *

pymysql.install_as_MySQLdb()


class Tianhua(object):
    def __init__(self, cli_df: pd.DataFrame, mut_df: pd.DataFrame,
                 here_df: pd.DataFrame, msi_df: pd.DataFrame,
                 tmb_df: pd.DataFrame, cnv_df: pd.DataFrame,
                 sv_df: pd.DataFrame, engine: sqlalchemy.engine.base.Engine):
        self.engine = engine
        self.th_sampleinf = self.clinical_preprocess(cli_df)
        self.th_filt_variations = self.variations_preprocess(mut_df)
        self.th_final_hereditary_tumor = self.hereditary_preprocess(here_df)
        self.msi_preprocess(msi_df)
        self.tmb_preprocess(tmb_df)
        self.th_filt_cnv = self.cnv_preprocess(cnv_df)
        self.th_filt_sv = self.fusion_preprocess(sv_df)

        self.add_ids()

    def clinical_preprocess(self, df: pd.DataFrame):
        new_cols = th_sampleinf_col[:-3]
        df.columns = new_cols

        return df

    # hasDrug字段待处理
    def variations_preprocess(self, df: pd.DataFrame):
        new_columns = th_filt_variations_col[:-3]

        df.columns = new_columns
        # need further process
        df['hasDrug'] = 'Y'

        return df

    # hasDrug字段待处理
    def hereditary_preprocess(self, df: pd.DataFrame):
        new_columns = th_final_hereditary_tumor_col[:-3]

        df.columns = new_columns
        df['hasDrug'] = 'Y'

        return df

    def msi_preprocess(self, df: pd.DataFrame):
        msi=''
        try:
            df = df.set_index('Level')
            msi = df.loc['Final_state','State']
        except:
            msi = ''
        
        self.th_sampleinf['msi'] =msi

    def tmb_preprocess(self, df: pd.DataFrame):
        tmb = ''
        for cell in df.iloc[:, 0]:
            res = re.findall('TMB=(.+)', str(cell))
            if res:
                tmb += res[0]

        self.th_sampleinf['tmb'] = tmb

    def cnv_preprocess(self, df: pd.DataFrame):
        new_columns = th_filt_cnv_col[:-3]
        df.columns = new_columns

        df['hasDrug'] = df.judge.map(lambda x: 'Y' if str(x) == '报' else 'N')

        return df

    def fusion_preprocess(self, df: pd.DataFrame):
        new_columns = th_filt_sv_col[:-3]
        df.columns = new_columns
        df['hasDrug'] = df.iloc[:, 0].map(lambda x: 'Y'
                                          if re.findall('^报', x) else 'N')

        return df

    def add_ids(self):
        # 查询当前五张表的最后状态
        try:
            th_sampleinf_max_id = int(
                self.engine.execute(
                    "select max(id) from th_sampleinf").fetchone()[0]) + 1

            if not th_sampleinf_max_id:
                th_sampleinf_max_id = 1
        except:
            th_sampleinf_max_id = 1

        try:
            th_filt_cnv_max_id = int(
                self.engine.execute(
                    "select max(id) from th_filt_cnv").fetchone()[0]) + 1
            if not th_filt_cnv_max_id:
                th_filt_cnv_max_id = 1
        except:
            th_filt_cnv_max_id = 1

        try:
            th_filt_sv_max_id = int(
                self.engine.execute(
                    "select max(id) from th_filt_sv").fetchone()[0]) + 1
            if not th_filt_sv_max_id:
                th_filt_sv_max_id = 1
        except:
            th_filt_sv_max_id = 1

        try:
            th_filt_variations_max_id = int(
                self.engine.execute("select max(id) from th_filt_variations").
                fetchone()[0]) + 1
            if not th_filt_variations_max_id:
                th_filt_variations_max_id = 1
        except:
            th_filt_variations_max_id = 1

        try:
            th_final_hereditary_tumor_max_id = int(
                self.engine.execute(
                    "select max(id) from th_final_hereditary_tumor").fetchone(
                    )[0]) + 1
            if not th_final_hereditary_tumor_max_id:
                th_final_hereditary_tumor_max_id = 1
        except:
            th_final_hereditary_tumor_max_id = 1

        self.th_sampleinf['id'] = range(
            th_sampleinf_max_id, th_sampleinf_max_id + len(self.th_sampleinf))
        self.th_filt_cnv['id'] = range(
            th_filt_cnv_max_id, th_filt_cnv_max_id + len(self.th_filt_cnv))
        self.th_filt_sv['id'] = range(th_filt_sv_max_id,
                                      th_filt_sv_max_id + len(self.th_filt_sv))

        self.th_filt_variations['id'] = range(
            th_filt_variations_max_id,
            th_filt_variations_max_id + len(self.th_filt_variations))
        self.th_final_hereditary_tumor['id'] = range(
            th_final_hereditary_tumor_max_id,
            th_final_hereditary_tumor_max_id +
            len(self.th_final_hereditary_tumor))

        self.th_filt_cnv['excel_id'] = self.th_sampleinf['id'].iloc[0]
        self.th_filt_sv['excel_id'] = self.th_sampleinf['id'].iloc[0]
        self.th_filt_variations['excel_id'] = self.th_sampleinf['id'].iloc[0]
        self.th_final_hereditary_tumor['excel_id'] = self.th_sampleinf[
            'id'].iloc[0]

    # th_filt_cnv, th_filt_sv, th_filt_variations, th_final_hereditary_tumor四张表中的hasDrug列更新
    def annotate(self, anno_df):
        target_list = [] if len(anno_df) == 0 else anno_df[[
            '检测内容', '检测结果c点'
        ]].drop_duplicates().apply(lambda x:
                                   (x['检测内容'], x['检测结果c点']), axis=1).tolist()
        self.th_filt_variations['hasDrug'] = self.th_filt_variations.apply(
            lambda x: 'Y' if (x['gene'], x['chgvs']) in target_list else 'N',
            axis=1)
        self.th_final_hereditary_tumor[
            'hasDrug'] = self.th_final_hereditary_tumor.apply(
                lambda x: 'Y'
                if (x['gene'], x['chgvs']) in target_list else 'N',
                axis=1)

        # verify if '报' can be the sign of cnv and sv

    def upload(self):
        self.add_ids()
        self.th_sampleinf.to_sql('th_sampleinf',
                                 con=self.engine,
                                 if_exists='append',
                                 index=False)
        self.th_filt_cnv.to_sql('th_filt_cnv',
                                con=self.engine,
                                if_exists='append',
                                index=False)
        self.th_filt_sv.to_sql('th_filt_sv',
                               con=self.engine,
                               if_exists='append',
                               index=False)
        self.th_filt_variations.to_sql('th_filt_variations',
                                       con=self.engine,
                                       if_exists='append',
                                       index=False)
        self.th_final_hereditary_tumor.to_sql('th_final_hereditary_tumor',
                                              con=self.engine,
                                              if_exists='append',
                                              index=False)
