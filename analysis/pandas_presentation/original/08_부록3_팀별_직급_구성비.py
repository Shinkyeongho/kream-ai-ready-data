# -*- coding: utf-8 -*-
"""
[부록 3] 팀별 직급 구성비
- 부서별 직급 7단계 100% 누적 가로막대 비율(%) 집계
"""
import pandas as pd

# 1. 정제 데이터 로드
df = pd.read_csv(r"data\Clean_(TO-BE)\clean_kream_inspection_joined.csv", low_memory=False)

# 2. 사번 기준 검수원 고유 마스터(2,960명) 추출
emp_master = df.drop_duplicates(subset=['INSPECTOR_EMP_NO']).copy()

# 3. 직급 7단계 정의
pos_order = ['주니어검수원', '일반검수원', '선임검수원', '책임감정사', '수석감정사', '파트장', '팀장']

# 4. 부서별 직급 구성비(%) 교차 집계 (행 기준 정규화 100%)
dept_emp_ratio = (pd.crosstab(
    emp_master['INSPECTOR_DEPT_NM'], 
    emp_master['INSPECTOR_POSITION_NM'], 
    normalize='index'
) * 100)[pos_order]

# 5. 총 등록인원 기준 내림차순 정렬
dept_counts = emp_master.groupby('INSPECTOR_DEPT_NM')['INSPECTOR_EMP_NO'].count()
dept_emp_ratio['총인원'] = dept_counts
dept_emp_ratio = dept_emp_ratio.sort_values(by='총인원', ascending=False).drop(columns='총인원').round(1)

print(dept_emp_ratio)
