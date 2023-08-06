#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : example
# @Time         : 2021/10/12 下午8:43
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
# import streamlit as st

from appzoo.apps_streamlit import st_pandas_profiling

st_pandas_profiling.app()
#
# st.markdown(
#     """
#     # 字段名检索
#     实现方式：simbert + ann
#     """
# )
#
# app_name = st.sidebar.selectbox('a', ['doc', '自动数据报告'])
#
# if app_name == '语义':
#     text = st.sidebar.text_input('字段', value="东北证券")  # st.text_area('xx', value="小米\n苹果")
#     topn = st.sidebar.slider('召回数', value=20, min_value=1, max_value=100)
# elif app_name == '自动数据报告':
#     # import pandas_profiling
#
#     from appzoo.apps_streamlit import st_pandas_profiling
#
#     # st_pandas_profiling.app()