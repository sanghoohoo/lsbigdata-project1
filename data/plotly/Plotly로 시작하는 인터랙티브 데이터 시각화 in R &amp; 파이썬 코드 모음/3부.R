## 3. df_covid19_100을 한국과 각 대륙별 열로 배치한 넓은 형태의 데이터프레임으로 변환
df_covid19_100_wide <- df_covid19_100 |>
  ## 날짜, 국가명, 확진자와, 백신접종완료자 데이터만 선택
  select(date, location, new_cases, people_fully_vaccinated_per_hundred) |>
  ## 열 이름을 적절히 변경
  rename('date' = 'date', '확진자' = 'new_cases', '백신접종완료자' =
           'people_fully_vaccinated_per_hundred') |>
  ## 넓은 형태의 데이터로 변환
  pivot_wider(id_cols = date, names_from = location,
              values_from = c('확진자', '백신접종완료자')) |>
  ## 날짜로 정렬
  arrange(date)
## 4. covid19 데이터를 국가별로 요약한 df_covid19_stat 생성
df_covid19_stat <- df_covid19 |>
  group_by(iso_code, continent, location) |>
  summarise(인구수 = max(population, na.rm = T),
            전체사망자수 = sum(new_deaths, na.rm = T),
            백신접종자완료자수 = max(people_fully_vaccinated, na.rm = T),
            인구백명당백신접종완료율 = max(people_fully_vaccinated_per_hundred, na.rm = T),
            인구백명당부스터접종자수 = max(total_boosters_per_hundred, na.rm = T)) |>
  ungroup() |>
  mutate(십만명당사망자수 = round(전체사망자수 / 인구수 *100000, 5),
         백신접종완료율 = 백신접종자완료자수 / 인구수)
## 여백 설정을 위한 변수 설정
margins_R <- list(t = 50, b = 25, l = 25, r = 25)

###############################################################################################
## 대학 학과 취업률 데이터 로딩
df_취업률 <- read_excel('./2021년 학과별 고등교육기관 취업통계.xlsx',
                     ## '학과별' 시트의 데이터를 불러오는데,
                     sheet = '학과별',
                     ## 앞의 13행을 제외하고
                     skip = 13,
                     ## 첫 번째 행은 열 이름으로 설정
                     col_names = TRUE,
                     ## 열의 타입을 설정, 처음 9개는 문자형으로, 다음 79개는 수치형으로 설정
                     col_types = c(rep('text', 9), rep('numeric', 79)))
## df_취업률에서 첫 번째부터 9번째까지의 열과 '계'로 끝나는 열을 선택하여 다시 df_취업률에 저장
df_취업률 <- df_취업률 |>
  select(1:9, ends_with('계'), '입대자')
## df_취업률에서 졸업자가 500명 이하인 학과 중 25% 샘플링
df_취업률_500 <- df_취업률 |>
  filter(졸업자_계 < 500) |>
  mutate(id = row_number()) |>
  filter(row_number() %in% seq(from = 1, to = nrow(df_취업률), by = 4))
## 열 이름을 적절히 설정
names(df_취업률_500)[10:12] <- c('졸업자수', '취업률', '취업자수')



###############################################################################################
if(!require(plotly)) { ## Plotly 로딩이 안 되면
  install.packages('plotly') ## Plotly 패키지 설치
  library(plotly) ## Plotly 패키지 로딩
}

###############################################################################################
## chap 7. 관계와 분포의 시각화
###############################################################################################
df_취업률_500 |>
  plot_ly() |>
  ## add_markers()로 marker mode의 scatter 트레이스 추가
  add_markers(x = ~졸업자수, y = ~취업자수, color = ~대계열) |>
  layout(title = list(text = '<b>졸업자 대비 취업자수</b>', font = list(color = 'white')),
         margin = margins_R,
         paper_bgcolor = 'black', plot_bgcolor = 'black',
         xaxis = list(color = 'white', ticksuffix = '명'),
         yaxis = list(color = 'white', gridcolor = 'gray', ticksuffix = '명', dtick = 100),
         legend = list(font = list(color = 'white')))

###############################################################################################
df_취업률_500 |>
  plot_ly() |>
  ## add_trace()로 marker mode의 scatter 트레이스 추가
  add_trace(type = 'scatter', mode = 'markers',
            x = ~졸업자수, y = ~취업자수, color = ~대계열) |>
  layout(
    ## 제목 설정
    title = list(text = '<b>졸업자 대비 취업자수</b>', font = list(color = 'white')),
    margin = margins_R, ## 여백 설정
    paper_bgcolor = 'black', plot_bgcolor = 'black', ## 여백 설정
    xaxis = list(color = 'white', ticksuffix = '명'), ## X축 설정
    ## Y축 설정
    yaxis = list(color = 'white', gridcolor = 'gray', ticksuffix = '명', dtick = 100),
    legend = list(font = list(color = 'white'))) ## 범례 설정

###############################################################################################
## 선형 회귀 모델 생성
lm_trend <- lm(data = df_취업률_500, 취업자수 ~ 졸업자수)

## 국소 회귀 모델 생성
loess_trend <- loess(data = df_취업률_500, 취업자수 ~ 졸업자수)
## 국소 회귀 모델 데이터 생성

df_loess_trend <- data.frame(X = df_취업률_500$졸업자수, Y = fitted(loess_trend)) |>
  arrange(X)

##
df_취업률_500 |>
  plot_ly(type = 'scatter', mode = 'markers') |>
  add_trace(x = ~졸업자수, y = ~취업자수, showlegend = FALSE) |>
  ## 선형 회귀 데이터를 사용하여 line mode scatter 트레이스 생성
  add_trace(mode = 'lines', x = ~졸업자수, y = ~fitted(lm_trend),
            name = '선형 추세선', line = list(dash = 'dot')) |>
  ## 국소 =회귀 데이터를 사용하여 line mode scatter 트레이스 생성
  add_trace(data = df_loess_trend, mode = 'lines',
            x = ~X, y = ~Y, name = 'loess 추세선')

###############################################################################################
p <- df_취업률_500 |>
  ggplot(aes(x = 졸업자수, y = 취업자수, color = 대계열)) +
  geom_point() +
  ## geom_smooth로 선형회귀 추세선 추가
  geom_smooth(method = 'lm', se = FALSE) +
  ## geom_smooth로 국소 회귀 추세선 추가
  geom_smooth(method = 'loess', se= FALSE, linetype = 2)

## ggplot2 객체를 Plotly로 전환
ggplotly(p)

###############################################################################################
df_covid19_stat |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'markers',
            x = ~백신접종완료율, y = ~인구백명당부스터접종자수,
            ## marker의 사이즈를 사용해 버블 차트 구현
            marker = list(size = ~십만명당사망자수, opacity = 0.5, sizemode = 'area')
  )

###############################################################################################
## 취업률 데이터를 사용해 Plotly 객체 생성
p_histogram <- df_취업률_500 |> plot_ly()

p_histogram |>
  ## histogram trace로 X축을 취업률로 매핑, name을 취업률로 설정
  add_histogram(x = ~취업률, name = '취업률',
                ## xbins 속성 설정
                xbins = list(start = 0, end = 100, size = 2.5)) |>
  ## 제목과 여백 설정
  layout(title = '취업률 histogram', margin = margins_R)

###############################################################################################
p_histogram <- df_취업률_500 |> plot_ly()

p_histogram |>
  ## histogram trace로 X축을 취업률로 매핑, name을 취업률로 설정
  add_histogram(x = ~취업률, color = ~과정구분, opacity = 0.4,
                xbins = list(size = 5)) |>
  layout(title = '취업률 histogram',
         ## histogram barmode를 "overlay"로 설정
         barmode = "overlay",
         margin = margins_R)

###############################################################################################
p_histogram <- df_취업률_500 |> plot_ly()
p_histogram |>
  add_histogram(x = ~취업률, name = '취업률',
                xbins = list(start = 0, end = 100, size = 2.5),
                ## 누적 히스토그램 설정
                cumulative = list(enabled=TRUE)) |>
  layout(title = '취업률 histogram', margin = margins_R)

###############################################################################################
#################
p_histogram |>
  add_trace(type = 'histogram', ## add_histogram()과 동의 함수
            x = ~대계열,
            ## 히스토그램 막대 함수를 'count'로 설정
            histfunc = 'count') |>
  layout(title = '취업률 histogram',
         yaxis = list(title = list(text = '학과수')),
         margin = margins_R)

#################
p_histogram |>
  add_trace(type = 'histogram', x = ~대계열, y = ~as.character(취업률),
            ## 히스토그램 막대 함수를 'sum'으로 설정
            histfunc = 'sum') |>
  ## Y축을 선형으로 설정
  layout(yaxis=list(type='linear',title = list(text = '취업률 합계')),
         title = '취업률 histogram',
         margin = margins_R)

#################
p_histogram |>
  add_trace(type = 'histogram', x = ~대계열, y = ~as.character(취업률),
            ## 히스토그램 막대 값을 'average'로 설정
            histfunc = 'avg') |>
  ## Y축을 선형으로 설정
  layout(yaxis=list(type='linear',title = list(text = '취업률 평균')),
         title = '취업률 histogram',
         margin = margins_R)

#################
p_histogram |>
  add_trace(type = 'histogram', x = ~대계열, y = ~as.character(취업률),
            ##히스토그램 막대 값을 'max'로 설정
            histfunc = 'max') |>
  ## Y축을 선형으로 설정
  layout(yaxis=list(type='linear',title = list(text = '취업률 최대값')),
         title = '취업률 histogram',
         margin = margins_R)

###############################################################################################
df_취업률 |>
  plot_ly() |>
  ## box 트레이스 생성
  add_boxplot(x = ~대계열, y = ~취업률_계)|>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

###############################################################################################
df_취업률 |>
  plot_ly() |>
  add_boxplot(x = ~대계열, y = ~취업률_계,
              ## boxmean과 notched 설정
              boxmean = 'sd', notched = TRUE)|>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

###############################################################################################
df_취업률 |>
  plot_ly() |>
  add_boxplot(x = ~대계열, y = ~취업률_계,
              ## color를 과정구분으로 매핑
              color = ~과정구분)|>
  ## boxmode를 group으로 설정
  layout(boxmode = "group", title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

###############################################################################################
fig <- df_covid19_100_wide |> plot_ly()

## 대륙별 확진자 box 트레이스 생성
fig <- fig |>
  add_boxplot(y = ~확진자_한국, name = '한국',
              ## boxpoints, jitter, pointpos 설정
              boxpoints = "all", jitter = 0.3, pointpos = -1.8)

fig <- fig |>
  add_boxplot(y = ~확진자_아시아, name = '아시아',
              boxpoints = "all", jitter = 0.3, pointpos = -1.8)

fig <- fig |>
  add_boxplot(y = ~확진자_유럽, name = '유럽',
              boxpoints = "all", jitter = 0.3, pointpos = -1.8)

fig <- fig |>
  add_boxplot(y = ~확진자_북미, name = '북미',
              boxpoints = "all", jitter = 0.3, pointpos = -1.8)

fig <- fig |>
  add_boxplot(y = ~확진자_남미, name = '남미',
              boxpoints = "all", jitter = 0.3, pointpos = -1.8)
fig <- fig |>
  add_boxplot(y = ~확진자_아프리카, name = '아프리카',
            boxpoints = "all", jitter = 0.3, pointpos = -1.8)

fig <- fig |>
  add_boxplot(y = ~확진자_오세아니아, name = '오세아니아',
              boxpoints = "all", jitter = 0.3, pointpos = -1.8)

fig |> layout(title = list(text = '한국 및 대륙별 일별 확진자 분포'),
              xaxis = list(title = '대륙명'),
              yaxis = list(title = '확진자수(명)'),
              margin = margins_R,
              paper_bgcolor='lightgray', plot_bgcolor='lightgray')

###############################################################################################
df_취업률_500 |>
  plot_ly() |>
  ## violin 트레이스 추가
  add_trace(type = 'violin', x = ~대계열, y = ~취업률) |>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

###############################################################################################
df_취업률_500 |>
  plot_ly() |>
  ## 바이올린 trace 추가
  add_trace(type = 'violin', x = ~대계열, y = ~취업률,
            ## 바이올린 내부 박스 표시
            box = list(visible = TRUE),
            ## 평균 선 표시
            meanline = list(visible = TRUE)) |>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

###############################################################################################
df_취업률_500 |>
  plot_ly() |>
  ## 대학과정을 필터링한 데이터 설정
  add_trace(data = df_취업률_500 |> filter(과정구분 == '대학과정'),
            ## 바이올린 trace로 추가
            type = 'violin', x = ~대계열, y = ~취업률, name = '대학',
            ## side, box의 설정
            side = 'positive', box = list(visible = TRUE, width = 0.5),
            ## meanline의 속성 설정
            meanline = list(visible = TRUE, width = 1)) |>
  ## 전문대학과정을 필터링한 데이터 설정
  add_trace(data = df_취업률_500 |> filter(과정구분 == '전문대학과정'),
            type = 'violin', x = ~대계열, y = ~취업률, name = '전문대학',
            side = 'negative', box = list(visible = TRUE, width = 0.5),
            meanline = list(visible = TRUE, width = 1)) |>
  ## violonemode 설정
  layout(violinmode = "overlay",
         title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

###############################################################################################
## chap 8. 비교와 구성의 시각화
###############################################################################################

###############################################################################################
df_취업률 |> group_by(대계열) |>
  summarise(취업률 = mean(취업률_계)) |>
  plot_ly() |>
  ## bar 트레이스 추가
  add_trace(type = 'bar', x = ~대계열, y = ~취업률,
            ## text와 textposition 설정
            text = ~취업률, textposition = 'inside',
            ## textemplate 설정
            texttemplate = '%{y:.1f}') |>
  layout(title = '계열별 취업률 평균',
         ## 눈금 접미어 설정
         yaxis = list(ticksuffix = '%'),
         margin = margins_R)

###############################################################################################
## 인구수가 백만명 이상의 국가중에 인구백명당접종완료율 top 10 필터링
vaccine_top10 <- df_covid19_stat |>
  filter(인구수 > 10000000) |>
  top_n(10, 인구백명당백신접종완료율)

vaccine_top10 |>
  plot_ly() |>
  add_trace(type = 'bar',
            x = ~location, y = ~인구백명당백신접종완료율,
            color = ~continent, text = ~인구백명당백신접종완료율,
            textposition = 'outside', texttemplate = '%{text}%',
            textfont = list(color = 'black')) |>
  layout(title = '완전 백신 접종률 상위 top 10 국가',
         xaxis = list(title = '국가명', categoryorder = 'total descending'),
         yaxis = list(title = '백신접종완료율', ticksuffix = '%'),
         margin = margins_R)

###############################################################################################
## 대륙별 백신접종완료율 top 5 필터링
vaccine_top5_by_continent <- df_covid19_stat |>
  filter(인구수 > 10000000, !is.na(continent)) |>
  group_by(continent) |>
  top_n(5, 인구백명당백신접종완료율) |>
  arrange(continent, desc(인구백명당백신접종완료율)) |>
  ungroup() |>
  mutate(seq = as.factor(seq(1:n())))

vaccine_top5_by_continent |>
  plot_ly(height = 800) |>
  add_trace(type = 'bar',
            y = ~seq, x = ~인구백명당백신접종완료율,
            color = ~continent,
            text = ~인구백명당백신접종완료율, textposition = 'outside',
            texttemplate = '%{text}%',
            textfont = list(color = 'black'),
            orientation = 'v'
  ) |>
  layout(title = '대륙별 완전 백신 접종률 상위 top 5 국가',
         xaxis = list(title = '백신접종완료율',
                      ticksuffix = '%', range = c(0, 105)),
         yaxis = list(title = '', autorange = 'reversed',
                      tickvals = ~seq, ticktext = ~location),
         margin = margins_R
  )

###############################################################################################
## 계열별 취업률을 넓은 데이터 형태로 전처리
취업률_by_계열 <- df_취업률 |>
  group_by(과정구분, 대계열) |>
  summarise(취업률 = mean(취업률_계)) |>
  pivot_wider(names_from = 과정구분, values_from = 취업률)

취업률_by_계열 |> plot_ly() |>
  ## 과정별로 bar 트레이스 추가
  add_trace(type = 'bar', x = ~대계열, y = ~ 전문대학과정, name = '전문대학과정') |>
  add_trace(type = 'bar', x = ~대계열, y = ~ 대학과정, name = '대학과정') |>
  add_trace(type = 'bar', x = ~대계열, y = ~대학원과정, name = '대학원과정') |>
  ## barmode, bargroupgap 설정
  layout(barmode = 'group', bargroupgap = 0.2,
         title = '계열별 교육과정별 취업률 평균',
         margin = margins_R)

###############################################################################################
vaccine_top10 |>
  plot_ly() |>
  ## bar 트레이스 추가
  add_trace(type = 'bar',
            x = ~location, y = ~인구백명당백신접종완료율,
            color = ~continent, text = ~인구백명당백신접종완료율,
            textposition = 'outside', texttemplate = '%{text}%',
            textfont = list(color = 'black')) |>
  ## markers+text 모드인 scatter 트레이스 생성
  add_trace(type = 'scatter', mode = 'markers+text',
            ## yaxis를 "y2"로 설정
            name = '10만명당 사망자수', yaxis = "y2",
            x = ~location,
            y = ~십만명당사망자수, text = ~round(십만명당사망자수, 1),
            textposition = 'top'
  )|>
  layout(title = '완전 백신 접종률 상위 top 10 국가',
         xaxis = list(title = '국가명', categoryorder = 'total descending'),
         yaxis = list(title = '백신접종완료율',
                      ticksuffix = '%'),
         ## y2 축의 설정
         yaxis2 = list(title = '인구10만명당 사망자수',
                       side = "right", overlaying = "y",
                       range = c(0, 300), ticksuffix = '명'),
         margin = margins_R, legend = list(x = 1.1))

###############################################################################################
vaccine_top5_by_continent |>
  plot_ly(height = 800) |>
  ## bar 트레이스 추가
  add_trace(type = 'bar',
            y = ~seq, x = ~인구백명당백신접종완료율, color = ~continent,
            text = ~인구백명당백신접종완료율, textposition = 'outside',
            texttemplate = '%{text}%',
            textfont = list(color = 'black'), orientation = 'v'
  ) |>
  ## markers+text 모드인 scatter 트레이스 생성
  add_trace(type = 'scatter', mode = 'markers+text',
            ## xaxis를 "x2"로 설정
            name = '사망자수', xaxis = "x2",
            y = ~seq, x = ~십만명당사망자수, color = I('black'),
            text = ~round(십만명당사망자수, 1),
            textposition = 'middle right')|>
  layout(barmode = 'group',
         title = list(text = '대륙별 완전 백신 접종률 상위 top 5 국가',
                      y = 0.97, yref = 'container'),
         xaxis = list(title = '백신접종완료율', range = c(0, 105),
                      ticksuffix = '%'),
         yaxis = list(title = '', autorange = 'reversed',
                      tickvals = ~seq, ticktext = ~location),
         ## xaxis2 축의 설정
         xaxis2 = list(title = list(text = '인구10만명당 사망자수',
                                    standoff = 1),
                       side = "top", overlaying = "x",
                       range = c(0, 700), ticksuffix = '명'),
         margin = list(r = 100, t = 80),
         height = 800)

###############################################################################################
## 비율 막대그래프를 위한 데이터 전처리
df_covid19_stat |>
  filter(iso_code %in% c('OWID_HIC', 'OWID_LIC', 'OWID_LMC', 'OWID_UMC')) |>
  select(3, 5, 6, 7) |>
  pivot_longer(cols = c(2, 3, 4)) |>
  pivot_wider(names_from = location) |>
  group_by(name) |>
  mutate(sum = (`High income`+`Low income`+`Lower middle income`+
                  `Upper middle income`)) |>
  mutate(`High income` = `High income` / sum,
         `Low income` = `Low income` / sum,
         `Lower middle income` = `Lower middle income` / sum,
         `Upper middle income` = `Upper middle income` / sum) |>
  plot_ly() |>
  ## 'High income'을 위한 bar 트레이스 추가
  add_trace(type = 'bar', x = ~`High income`, y = ~name,
            name = 'High income', orientation = 'h',
            marker = list(line = list(color = 'white', width = 2))) |>
  ## 'Upper middle income'을 위한 bar 트레이스 추가
  add_trace(type = 'bar', x = ~`Upper middle income`, y = ~name,
            name = 'Upper middle income', orientation = 'h',
            marker = list(line = list(color = 'white', width = 2))) |>
  ## 'Lower middle income'을 위한 bar 트레이스 추가
  add_trace(type = 'bar', x = ~`Lower middle income`, y = ~name,
            name = 'Lower middle income', orientation = 'h',
            marker = list(line = list(color = 'white', width = 2))) |>
  ## 'Low income'을 위한 bar 트레이스 추가
  add_trace(type = 'bar', x = ~`Low income`, y = ~name,
            name = 'Low income', orientation = 'h',
            marker = list(line = list(color = 'white', width = 2))) |>
  ## 'High income' 값 표시를 위한 주석 레이어 추가
  add_annotations(xref = 'x', yref = 'y',
                  x = ~`High income` / 2, y = ~name,
                  text = ~paste(round(`High income`*100, 1), '%'),
                  font = list(color = 'white'),
                  showarrow = FALSE) |>
  ## 'High income' 값 표시를 위한 주석 레이어 추가
  add_annotations(xref = 'x', yref = 'y',
                  x = ~`High income` + `Upper middle income` / 2, y = ~name,
                  text = ~paste(round(`Upper middle income`*100, 1), '%'),
                  font = list(color = 'white'),
                  showarrow = FALSE) |>
  ## 'High income' 값 표시를 위한 주석 레이어 추가
  add_annotations(xref = 'x', yref = 'y',
                  x = ~`High income` + `Upper middle income` + 
                    `Lower middle income` / 2,
                  y = ~name,
                  text = ~paste(round(`Lower middle income`*100, 1), '%'),
                  font = list(color = 'white'),
                  showarrow = FALSE) |>
  add_annotations(xref = 'x', yref = 'y',
                  x = ~`High income` + `Upper middle income` + 
                    `Lower middle income` + `Low income` / 2, y = ~name,
                  text = ~paste(round(`Low income`*100, 1), '%'),
                  font = list(color = 'white'),
                  showarrow = FALSE) |>
  layout(barmode = 'stack',
         title = '국가 소득 구간별 코로나19 현황',
         xaxis = list(title = '', tickformat = '.0%'),
         yaxis = list(title = ''),
         legend = list(orientation = 'h', traceorder = 'normal'),
         margin = margins_R)

###############################################################################################
## 롤리팝 그래프를 위한 데이터 전처리
df_lolipop <- df_covid19_stat |>
  filter(인구수 > 5000000, continent == 'Asia') |>
  arrange(desc(인구백명당백신접종완료율))

df_lolipop |>
  plot_ly(x = ~reorder(location, desc(인구백명당백신접종완료율))) |>
  ## 세그먼트 레이어 추가
  add_segments(xend = ~reorder(location, desc(인구백명당백신접종완료율)),
               y = ~인구백명당백신접종완료율,
               yend = 0, color = I('gray'),
               showlegend = FALSE) |>
  ## markers 모드인 scatter 트레이스 추가
  add_trace(type = 'scatter', mode = 'markers', name = '접종완료율',
            y = ~인구백명당백신접종완료율, color = I('darkblue')) |>
  add_trace(type = 'scatter', mode = 'markers',
            symbol = I('circle-open'),
            name = '사망자수', yaxis = "y2",
            y = ~십만명당사망자수, color = I('black'),
            text = ~round(십만명당사망자수, 1),
            textposition = 'right')|>
  layout(barmode = 'group',
         title = list(text = '아시아 국가의 백신접종율',
                      y = 0.97, yref = 'container'),
         yaxis = list(title = '백신접종완료율', range = c(0, 105),
                      ticksuffix = '%'),
         xaxis = list(title = ''),
         ## 두 번째 Y축의 설정
         yaxis2 = list(title = list(text = '인구10만명당 사망자수',
                                    standoff = 10),
                       side = "right", overlaying = "y",
                       range = c(0, 200), ticksuffix = '명'),
         margin = margins_R,
         legend = list(orientation = 'h', y = -0.5, x = 0.5,
                       yref = 'container', xanchor = 'center'),
         showlegend = T)

###############################################################################################
## 레이더 차트를 위한 데이터 전처리
df_radar_veccine <- df_covid19_stat |>
  filter(iso_code %in% c('OWID_AFR', 'OWID_ASI', 'OWID_EUR', 
                         'OWID_NAM', 'OWID_OCE', 'OWID_SAM')) |>
  select(continent, location, 인구백명당백신접종완료율)

df_radar_veccine |>
  plot_ly() |>
  ## scatterpolar 트레이스 추가
  add_trace(type = 'scatterpolar',
            theta = ~location, r = ~인구백명당백신접종완료율, 
            fill = 'toself') |>
  ## polar 속성 설정
  layout(polar = list(
    ## angularaxis 속성 설정
    angularaxis = list(
      ticktext = c('아프리카', '아시아', '유럽', '북미', 
                   '오세아니아', '남미'),
      tickvals = c('Africa', 'Asia', 'Europe', 'North America', 
                   'Oceania', 'South America'),
      linewidth = 2, linecolor = 'black', gridcolor = 'gray'),
    ## radialaxis 속성 설정
    radialaxis = list(linewidth = 2, linecolor = 'dodgerblue', 
                      gridcolor = 'skyblue', nticks = 5, 
                      ticksuffix = '%', title = '백신 접종률')),
    title = list(text = '대륙별 백신 접종률', x = 0.5),
    margin = margins_R)

###############################################################################################
## 덤벨 차트를 위한 데이터 전처리
df_covid19_stat |>
  filter(!is.na(continent), 인구수 > 10000000) |>
  group_by(continent) |>
  summarise(min = min(십만명당사망자수), max = max(십만명당사망자수)) |>
  plot_ly() |>
  ## 덤벨 차트용 세그먼트 추가
  add_segments(
             x = ~min, xend = ~max, y = ~continent, yend = ~continent,
             showlegend = FALSE,
             color = I('gray')) |>
  ## 최소값 트레이스 추가
  add_trace(type = 'scatter', mode = 'markers+text',
            x = ~min, y = ~continent, name = '최소',
            text = ~round(min, 1), textposition = 'bottom center',
            color = I('#1f77b4')) |>
  ## 최대값 트레이스 추가
  add_trace(type = 'scatter', mode = 'markers+text',
            x = ~max, y = ~continent, name = '최대',
            text = ~round(max, 1), textposition = 'bottom center',
            color = I('darkblue'), symbol = I('circle-open')) |>
  layout(title = '대륙별 10만명당 사망자수 차이',
         xaxis = list(title = '10만명당 사망자수'),
         yaxis = list(title = '', autorange = 'reversed'),
         margin = margins_R)

###############################################################################################
df_취업률_500 |> group_by(대계열) |>
  summarise(졸업자수 = sum(졸업자수)) |>
  plot_ly() |>
  ## value와 labels를 매핑한 파이 trace 추가
  add_trace(type = 'pie', values = ~졸업자수, labels = ~대계열, direction = 'clockwise') |>
  layout(title = list(text = '대학 계열별 졸업생 분포'),
         margin = margins_R)

###############################################################################################
p_pie <- df_취업률_500 |> group_by(대계열) |>
  summarise(졸업자수 = sum(졸업자수)) |>
  plot_ly()

p_pie |>
  ## value를 매핑한 파이 trace 추가
  add_trace(type = 'pie', values = ~졸업자수, labels = ~대계열, direction = 'clockwise',
            textinfo = 'value') |>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

p_pie |>
  ## value와 percent를 매핑한 파이 trace 추가
  add_trace(type = 'pie', values = ~졸업자수, labels = ~대계열, direction = 'clockwise',
            textinfo = 'value+percent') |>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

p_pie |>
  ## value와 labels를 매핑한 파이 trace 추가
  add_trace(type = 'pie', values = ~졸업자수, labels = ~대계열, direction = 'clockwise',
            textinfo = 'label+value') |>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

p_pie |>
  ## label과 percent를 매핑한 파이 trace 추가
  add_trace(type = 'pie', values = ~졸업자수, labels = ~대계열, direction = 'clockwise',
            textinfo = 'label+percent') |>
  layout(title = list(text = '대학 계열별 취업률 분포'),
         margin = margins_R)

###############################################################################################
p_pie |>
  add_trace(type = 'pie', values = ~졸업자수, labels = ~대계열, direction = 'clockwise',
            ## hole을 사용한 도넛 차트
            textinfo = 'value', hole = 0.3) |>
  add_annotations(x = 0.5, y = 0.5, text = '<b>졸업생수</b>',
                  showarrow = FALSE, xanchor = 'center',
                  font = list(size = 20)) |>
  layout(title = list(text = '대학 계열별 졸업생 분포'),
         margin = margins_R)

###############################################################################################
p_pie |>
  add_trace(type = 'pie', values = ~졸업자수, labels = ~대계열, direction = 'clockwise',
            textinfo = 'value', hole = 0.3,
            ## 파이 차트 강조 설정
            pull = c(0, 0.2, 0, 0, 0, 0, 0)) |>
  add_annotations(x = 0.5, y = 0.5, text = '<b>졸업생수</b>',
                  showarrow = FALSE, xanchor = 'center',
                  font = list(size = 20)) |>
  layout(title = list(text = '대학 계열별 졸업생 분포'),
         margin = margins_R)

###############################################################################################
## 선버스트 차트를 위한 데이터 전처리
df_sunburst <- df_취업률_500 |> group_by(대계열, 중계열) |>
  summarise(졸업자수 = sum(졸업자수))

all_sum <- sum(df_sunburst$졸업자수)

계열_sum <- df_sunburst |> group_by(대계열) |>
  summarise(sum = sum(졸업자수)) |>
  select(sum) |> pull()

df_sunburst |> plot_ly() |>
  add_trace(type = 'sunburst',
            ## sunburst 트레이스의 labels 설정
            labels = c('전체', unique(df_sunburst$대계열), df_sunburst$중계열),
            ## sunburst 트레이스의 parents 설정
            parents = c('', rep('전체', 7), df_sunburst$대계열),
            ## sunburst 트레이스의 values 설정
            values = c(all_sum, 계열_sum, df_sunburst$졸업자수),
            branchvalues = 'total')

###############################################################################################
###### branchvalues = 'total' 선버스트 차트
df_sunburst |> plot_ly() |>
  add_trace(type = 'sunburst',
            labels = c('전체', unique(df_sunburst$대계열), df_sunburst$중계열),
            parents = c('', rep('전체', 7), df_sunburst$대계열),
            values = c(all_sum, 계열_sum, df_sunburst$졸업자수),
            branchvalues = 'total', maxdepth = 3)

## branchvalues = 'reminder' 선버스트 차트
df_sunburst |> plot_ly() |>
  add_trace(type = 'sunburst',
            labels = c('전체', unique(df_sunburst$대계열), df_sunburst$중계열),
            parents = c('', rep('전체', 7), df_sunburst$대계열),
            values = c(all_sum, 계열_sum, df_sunburst$졸업자수),
            branchvalues = 'remainder', maxdepth = 3)

###############################################################################################
## insidetextorientation = 'radial' 선버스트 차트
df_sunburst |> plot_ly() |>
  add_trace(type = 'sunburst',
            labels = c('전체', unique(df_sunburst$대계열), df_sunburst$중계열),
            parents = c('', rep('전체', 7), df_sunburst$대계열),
            values = c(all_sum, 계열_sum, df_sunburst$졸업자수),
            branchvalues = 'total', insidetextorientation = 'radial', maxdepth = 3)

## insidetextorientation = 'horizontal' 선버스트 차트
df_sunburst |> plot_ly() |>
  add_trace(type = 'sunburst',
            labels = c('전체', unique(df_sunburst$대계열), df_sunburst$중계열),
            parents = c('', rep('전체', 7), df_sunburst$대계열),
            values = c(all_sum, 계열_sum, df_sunburst$졸업자수),
            branchvalues = 'total', insidetextorientation = 'horizontal',maxdepth = 3)

###############################################################################################
plot_ly() |>
  add_trace(type = 'treemap',
            ## treemap 트레이스의 labels 설정
            labels = c('전체', unique(df_sunburst$대계열), df_sunburst$중계열),
            ## treemap 트레이스의 parents 설정
            parents = c('', rep('전체', 7), df_sunburst$대계열),
            ## treemap 트레이스의 values 설정
            values = c(all_sum, 계열_sum, df_sunburst$졸업자수),
            textinfo = 'label+value+percent parent+percent entry')

###############################################################################################
## chap 9. 시간과 흐름의 시각화
###############################################################################################
###############################################################################################
## 5개국 데이터로 전처리
total_deaths_5_nations_by_day <- df_covid19 |>
  filter((iso_code %in% c('KOR', 'USA', 'JPN', 'GBR', 'FRA'))) |>
  filter(!is.na(total_deaths_per_million))

total_deaths_5_nations_by_day |>
  plot_ly() |>
  ## scatter 트레이스 생성
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  ## layout의 제목, 축제목, 여백 속성 설정
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = ''),
         yaxis = list(title = '10만명당 사망자수 누계'),
         margin = margins_R)

###############################################################################################
## 마지막 일로부터 180일 후 날짜 계산
last_day = max(distinct(total_deaths_5_nations_by_day, date) |> pull()) + 180

total_deaths_5_nations_by_day |>
  plot_ly() |>
  ## scatter 트레이스 생성
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  ## 각국의 마지막 일옆에 국가명 주석 추가
  add_annotations(
    x =~ (total_deaths_5_nations_by_day |> filter(date == max(date)) |>
            select(date) |> pull()),
    y = ~(total_deaths_5_nations_by_day |> filter(date == max(date)) |>
            select(total_deaths_per_million) |> pull()),
    text = ~(total_deaths_5_nations_by_day |> filter(date == max(date)) |>
               select(location) |> pull()),
    textposition = 'middle right', xanchor = 'left', showarrow = FALSE
  ) |>
  ## 설날 주석을 추가
  add_annotations(
    x = '2022-02-01',
    y = ~(total_deaths_5_nations_by_day |>
            filter(date == '2022-02-01', iso_code == 'KOR') |>
            select(total_deaths_per_million) |> pull()),
    text = '설날',
    textposition = 'middle right', xanchor = 'right'
  ) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = '',
                      range = c('2020-02-15', format(last_day, format="%Y-%m-%d"))),
         yaxis = list(title = '10만명당 사망자수 누계'),
         margin = margins_R,
         showlegend = FALSE)

###############################################################################################
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T
  ) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = '',
                      ## rangeslider 속성 설정
                      rangeslider = list(visible = T)),
         yaxis = list(title = '10만명당 사망자수 누계'),
         showlegend = T, margin = margins_R,
         title = 'Time Series with Rangeslider')

###############################################################################################
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million , linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         yaxis = list(title = '10만명당 사망자수 누계'),
         xaxis = list(title = '',
                      range = c(min(total_deaths_5_nations_by_day$date),
                                max(total_deaths_5_nations_by_day$date)),
                      ## rangeslider 속성 설정
                      rangeslider = list(visible = T),
                      ## rangeselector 속성 설정
                      rangeselector=list(
                        ## rangeselector의 buttons 속성 설정
                        buttons=list(
                          list(count=7, label='1 Week before', step='day', stepmode='backward'),
                          list(count=1, label='1 month before', step='month', stepmode='backward'),
                          list(count=6, label='6 months before', step='month', stepmode='backward'),
                          list(count=1, label='new years day', step='year', stepmode='todate'),
                          list(count=1, label='1 year before', step='year', stepmode='backward')
                        ))),
         showlegend = T, margin = list(t = 75, b = 25, l = 25, r = 25))

###############################################################################################
## 호버모드가 x인 시각화
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = ''),
         yaxis = list(title = '10만명당 사망자수 누계'),
         margin = margins_R,
         ## 호버 모드 설정
         hovermode="x")

## 호버모드가 y인 시각화
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = ''),
         yaxis = list(title = '10만명당 사망자수 누계'),
         margin = margins_R,
         ## 호버 모드 설정
         hovermode="y")

## 호버모드가 x unified인 시각화
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = ''),
         yaxis = list(title = '10만명당 사망자수 누계'),
         margin = margins_R,
         ## 호버 모드 설정
         hovermode="x unified")

## 호버모드가 y unified인 시각화
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = ''),
         yaxis = list(title = '10만명당 사망자수 누계'),
         margin = margins_R,
         ## 호버 모드 설정
         hovermode="y unified")

###############################################################################################
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million , linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = '',
                      ## X축의 spikemode 설정
                      spikemode = 'across'),
         yaxis = list(title = '10만명당 사망자수 누계',
                      ## Y축의 spikemode 설정
                      spikemode = 'toaxis'),
         hovermode='x',
         margin = margins_R)

###############################################################################################
total_deaths_5_nations_by_day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million , linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = '', spikemode = 'across',
                      ## X축 눈금 라벨 설정
                      tickformat = '%Y년 %m월',
                      ## X축 눈금 간격 설정
                      dtick = 'M3'),
         yaxis = list(title = '10만명당 사망자수 누계',
                      spikemode = 'toaxis'),
         hovermode = 'x',
         margin = margins_R)

###############################################################################################
total_deaths_5_nations_by_day |>
  ## Plotly 객체 생성
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million , linetype = ~location, connectgaps = T) |>
  layout(title = '코로나19 사망자수 추세',
         xaxis = list(title = '', spikemode = 'across', tickformat = '%Y년 %m월',
                      ## tickformatstops 설정
                      tickformatstops = list(
                        ## 1000밀리초까지의 tickformat
                        list(dtickrange=list(NULL, 1000), value="%H:%M:%S.%L 밀리초"),
                        ## 1초 ~ 1분까지의 tickformat
                        list(dtickrange=list(1000, 60000), value="%H:%M:%S 초"),
                        ## 1분 ~ 1시간까지의 tickformat
                        list(dtickrange=list(60000, 3600000), value="%H:%M 분"),
                        ## 1시간 ~ 1일까지의 tickformat
                        list(dtickrange=list(3600000, 86400000), value="%H:%M 시"),
                        ## 1일 ~ 1주까지의 tickformat
                        list(dtickrange=list(86400000, 604800000), value="%e. %b 일"),
                        ## 1주 ~ 1월까지의 tickformat
                        list(dtickrange=list(604800000, "M1"), value="%e. %b 주"),
                        ## 1월 ~ 1년까지의 tickformat
                        list(dtickrange=list("M1", "M12"), value="%b '%y 월"),
                        ## 1년 이상의 tickformat
                        list(dtickrange=list("M12", NULL), value="%Y 년")
                      )),
         yaxis = list(title = '10만명당 사망자수 누계',
                      spikemode = 'toaxis'),
         hovermode = 'x',
         margin = margins_R)

###############################################################################################
if (!require ("tqk")) {
  if (!require("remotes")) {
    install.packages("remotes")
  }
  remotes::install_github("mrchypark/tqk")
  library('tqk')
}

###############################################################################################
## 관련 패키지 로딩
library(tqk)
library(lubridate)
## 주가 코드를 가져옴
code <- code_get()

start_day = as.Date('2022-10-07')
end_day = start_day + 100

## 삼성전자의 최근 100일 주가를 가져옴
samsung <- tqk_get('005930', from=start_day, to=end_day)
samsung |> head()

###############################################################################################
samsung |> plot_ly() |>
  add_trace(
    ## candlestick 트레이스를 추가
    type="candlestick", x = ~date,
    ## OHLC 데이터 설정
    open = ~open, close = ~close,
    high = ~high, low = ~low) |>
  layout(title = "삼성전자 Candlestick Chart",
         margin = margins_R)

###############################################################################################
samsung |> plot_ly() |>
  add_trace(
    type="candlestick", x = ~date,
    open = ~open, close = ~close,
    high = ~high, low = ~low,
    ## 상승 시 선 색상 설정
    increasing = list(line = list(color = 'red')),
    ## 하락 시 선 색상 설정
    decreasing = list(line = list(color = 'blue'))) |>
  layout(title = "삼성전자 Candlestick Chart",
         ## rangeslider는 안 보이도록 설정
         xaxis = list(rangeslider = list(visible = F)),
         margin = margins_R)

###############################################################################################
fig1 <- samsung |> plot_ly() |>
  add_trace(
    type="candlestick", x = ~date,
    open = ~open, close = ~close,
    high = ~high, low = ~low,
    increasing = list(line = list(color = 'red')),
    decreasing = list(line = list(color = 'blue'))) |>
  layout(title = "삼성전자 Candlestick Chart",
         xaxis = list(rangeslider = list(visible = F)),
         yaxis = list(title = '주가'),
         showlegend = FALSE)

## 거래량 막대그래프인 bar 트레이스 추가
fig2 <- samsung %>% plot_ly() |>
  add_trace(type = 'bar', x=~date, y=~volume, type='bar',
            color = I('gray'), showlegend = FALSE) |>
  layout(yaxis = list(title = '거래량'))

## 서브플롯으로 거래량 그래프 설정
subplot(fig1, fig2, heights = c(0.7,0.2), nrows=2, shareX = TRUE) |>
  layout(margin = margins_R)

###############################################################################################
fig1 <- samsung |> plot_ly() |>
  add_trace(
    type="candlestick", x = ~date,
    open = ~open, close = ~close,
    high = ~high, low = ~low,
    increasing = list(line = list(color = 'red')),
    decreasing = list(line = list(color = 'blue'))
  ) |>
  layout(title = "삼성전자 Candlestick Chart",
         xaxis = list(rangeslider = list(visible = F),
                      ## rangebreaks 설정
                      rangebreaks=list(
                        ## 주말 제거
                        list(bounds=list("sat", "mon")),
                        ## 특정 공휴일 제거
                        list(values = list("2022-09-09", "2022-09-12", "2022-10-03", "2022-10-10",
                                           "2022-12-30"))
                      )),
         yaxis = list(title = '주가'),
         showlegend = FALSE)

fig2 <- samsung %>% plot_ly() |>
  add_trace(type = 'bar', x=~date, y=~volume, type='bar',
            color =I('gray'), showlegend = FALSE) |>
  layout(xaxis = list(rangebreaks=list( ## rangebreaks 설정
    ## 주말 제거
    list(bounds=list("sat", "mon")),
    ## 특정 공휴일 제거
    list(values = list("2022-09-09", "2022-09-12", "2022-10-03", "2022-10-10", "2022-12-30"))
  )),
  yaxis = list(title = '거래량'))

subplot(fig1, fig2, heights = c(0.7,0.2), nrows=2, shareX = TRUE) |>
  layout(margin = margins_R)

###############################################################################################
## 최근 100일간의 우리나라 코로나19 신규확진자 데이터 전처리
total_deaths_5_nations_since_100day <- total_deaths_5_nations_by_day |>
  filter((iso_code %in% c('KOR'))) |>
  filter(date > max(date)-100)

## 주말이 포함된 scatter 트레이스 생성
p1 <- total_deaths_5_nations_since_100day |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~new_cases , color = I('darkblue'), connectgaps = T)

## 주말이 제거된 scatter 트레이스 생성
p2 <- total_deaths_5_nations_since_100day |>
  filter((iso_code %in% c('KOR'))) |>
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~new_cases , color = I('darkblue'), connectgaps = T) |>
  layout(xaxis = list(rangebreaks=list(list(bounds=list("sun", "tue")),
                                       list(values=list('2022-03-02'))
  )))

## 서브플롯 생성
subplot(
  p1 |> layout(annotations = list(x = 0.5 , y = 1.05,
                                  text = "주말이 포함된 확진자수", showarrow = F,
                                  xref='paper', yref='paper', xanchor = 'center')),
  p2 |> layout(annotations = list(x = 0.5 , y = 1.05,
                                  text = "주말이 제거된 확진자수", showarrow = F,
                                  xref='paper', yref='paper', xanchor = 'center')),
  nrows = 2, margin = 0.05) |>
  layout(title = '우리나라의 코로나19 확진자수 추세', hovermode = "x unified",
         margin = margins_R, showlegend = FALSE)

###############################################################################################
## zoo 패키지 설치 및 로딩
if(!require(zoo)) {
  install.packages('zoo')
  library(zoo)
}

## 5일, 20일, 40일 이동평균 산출
samsung_moving <- samsung %>%
  mutate(MA_5 = zoo::rollmean(x = close, k = 5, 
                              align = "right", fill = NA),
         MA_20 = zoo::rollmean(x = close, k = 20, 
                               align = "right", fill = NA),
         MA_40 = zoo::rollmean(x = close, k = 40, 
                               align = "right", fill = NA))

## casdlestick 트레이스 생성
fig1 <- samsung_moving |> plot_ly() |>
  add_trace(
    type="candlestick", x = ~date,
    open = ~open, close = ~close,
    high = ~high, low = ~low,
    increasing = list(line = list(color = 'red')),
    decreasing = list(line = list(color = 'blue')),
    showlegend = FALSE
  ) |>
  layout(title = "삼성전자 Candlestick Chart",
         xaxis = list(rangeslider = list(visible = F),
                      rangebreaks=list(
                        list(bounds=list("sat", "mon")),
                        list(values = list("2022-09-09", "2022-09-12", "2022-10-03", "2022-10-10",
                                           "2022-12-30"))
                      )),
         yaxis = list(title = '주가'))

## 5일 이동평균선 추가
fig1 <- fig1 |> add_trace(type = 'scatter', mode = 'lines',
                          line = list(dash = 'solid'),
                          x = ~date, y = ~MA_5, name = '5일 이동평균')

## 20일 이동평균선 추가
fig1 <- fig1 |> add_trace(type = 'scatter', mode = 'lines',
                          line = list(dash = 'dash'),
                          x = ~date, y = ~MA_20, name = '20일 이동평균')

## 40일 이동평균선 추가
fig1 <- fig1 |> add_trace(type = 'scatter', mode = 'lines',
                          line = list(dash = 'dot'),
                          x = ~date, y = ~MA_40, name = '40일 이동평균')

## 거래량 그래프 추가
fig2 <- samsung %>% plot_ly() |>
  add_trace(type = 'bar', x=~date, y=~volume, type='bar',
            color =I('gray'), showlegend = FALSE) |>
  layout(xaxis = list(rangebreaks=list(
    list(bounds=list("sat", "mon")),
    list(values = list("2022-09-09", "2022-09-12", "2022-10-03", "2022-10-10", "2022-12-30"))
  )),
  yaxis = list(title = '거래량'))

## 서브플롯 설정
subplot(fig1, fig2, heights = c(0.7,0.2), nrows=2, shareX = TRUE) |>
  layout(margin = margins_R)

###############################################################################################
## 전일 종가 대비 등락가 전처리
fig <- samsung |> mutate(lag = close - lag(close)) |>
  plot_ly()

## waterfall 트레이스 생성
fig |> add_trace(type = 'waterfall',
                 name = "등락", orientation = "v",
                 x = ~date, y = ~lag,
                 increasing = list(marker = list(color = 'red')),
                 decreasing = list(marker = list(color = 'blue')
                 )
  ) |>
  layout(xaxis = list(rangeslider = list(visible = FALSE),
                      rangebreaks = list(
                        list(bounds=c("sat", "mon")),
                        list(values=c("2022-09-09", "2022-09-12", "2022-10-03", "2022-10-10"))
                      )),
         yaxis = list(title_text="주가 등락(원)"),
         title = list(text = "삼성전자 주가 Waterfall Chart", x = 0.5),
         showlegend = FALSE, margin = margins_R)

###############################################################################################
## 퍼널 차트를 위한 데이터 전처리
df_funnel <- df_취업률 |>
  summarise(전체취업자 = sum(`취업자_교외취업자_계` + `취업자_교내취업자_계`),
            유지취업자_1차 = sum(`1차 유지취업자_계`),
            유지취업자_2차 = sum(`2차 유지취업자_계`),
            유지취업자_3차 = sum(`3차 유지취업자_계`),
            유지취업자_4차 = sum(`4차 유지취업자_계`),
  ) |>
  pivot_longer(1:5, names_to = '구분', values_to = '유지취업자')

## funnel 트레이스 생성
df_funnel |>
  plot_ly() |>
  add_trace(type = 'funnel', x = ~유지취업자, y = ~구분,
            text = ~유지취업자, textinfo = "text+percent initial") |>
  layout(title = '유지취업자 Funnel Chart',
         yaxis = list(categoryorder = "total descending"),
         margin = margins_R)

###############################################################################################
## stack funnel 트레이스를 위한 전문대학 데이터 전처리
df_funnel_전문대학 <- df_취업률 |>
  filter(과정구분 == '전문대학과정') |>
  summarise(전체취업자 = sum(`취업자_교외취업자_계` + `취업자_교내취업자_계`),
            유지취업자_1차 = sum(`1차 유지취업자_계`),
            유지취업자_2차 = sum(`2차 유지취업자_계`),
            유지취업자_3차 = sum(`3차 유지취업자_계`),
            유지취업자_4차 = sum(`4차 유지취업자_계`),
  ) |>
pivot_longer(1:5, names_to = '구분', values_to = '유지취업자')

## stack funnel 트레이스를 위한 대학 데이터 전처리
df_funnel_대학 <- df_취업률 |>
  filter(과정구분 == '대학과정') |>
  summarise(전체취업자 = sum(`취업자_교외취업자_계` + `취업자_교내취업자_계`),
            유지취업자_1차 = sum(`1차 유지취업자_계`),
            유지취업자_2차 = sum(`2차 유지취업자_계`),
            유지취업자_3차 = sum(`3차 유지취업자_계`),
            유지취업자_4차 = sum(`4차 유지취업자_계`),
  ) |>
  pivot_longer(1:5, names_to = '구분', values_to = '유지취업자')

## stack funnel 트레이스 생성
df_funnel_전문대학 |>
  plot_ly() |>
  add_trace(type = 'funnel', name = '전문대학',
            x = ~유지취업자, y = ~구분,
            text = ~유지취업자, textinfo = "text+percent initial") |>
  add_trace(data = df_funnel_대학, type = 'funnel', name = '대학',
            x = ~유지취업자, y = ~구분,
            text = ~유지취업자, textinfo = "text+percent initial") |>
  layout(title = '유지취업자 Funnel Chart',
         yaxis = list(categoryorder = "total descending"),
         margin = margins_R)

###############################################################################################
## funnelarea 트레이스를 위한 데이터 전처리
df_funnelarea <- df_covid19_100_wide |>
  summarise(아프리카 = sum(확진자_아프리카),
            아시아 = sum(확진자_아시아),
            유럽 = sum(확진자_유럽),
            북미 = sum(확진자_북미),
            남미 = sum(확진자_남미),
            오세아니아 = sum(확진자_오세아니아)) |>
  pivot_longer(1:6, names_to = '대륙', values_to = '전체확진자')

## funnelarea 트레이스 생성
df_funnelarea |>
  plot_ly() |>
  add_trace(type = 'funnelarea', text = ~대륙, values = ~전체확진자,
            textinfo = "text+value+percent") |>
  layout(title = '최근 100일간 대륙별 확진자수 Funnelarea 차트',
         margin = margins_R)

###############################################################################################
df_sankey <- df_취업률 |>
  ## 열 중에서 3열(과정구분, 왼쪽 노드로 사용)과 12열, 21열부터 26열(오른쪽 노드로 사용)까지를 선택
select(3, 12, 21:26) |>
  ## 과정구분 열을 사용하여 그룹화
  group_by(과정구분) |>
  ## 전체 열에 대해 `sum`을 적용(summarise_all은 전체 열에 동일한 요약함수를 적영하는 함수임)
  summarise_all(sum) |>
  ## 열 이름을 적절히 변경
  rename(c('취업' = '취업자_합계_계', '진학' = '진학자_계', '취업불가' = '취업불가능자_계',
           '외국인' = '외국인유학생_계', '제외인정' = '제외인정자_계', '기타' = '기타_계', '미상' =
             '미상_계')) |>
  ## 첫 번째 열을 제외하고 나머지 열들에 긴 형태의 데이터로 변환, 열 이름이 들어간 열은 '구분'으로 데이터 값이 들어간 열은 '학생수'열로 설정
pivot_longer(cols = 2:8, names_to = '졸업구분', values_to = '학생수') |>
  ## 과정구분 열과 구분 열의 순서설정을 위해 팩터 레벨 설정
  mutate(과정구분_node = case_when(
    과정구분 == '전문대학과정' ~ 0,
    과정구분 == '대학과정' ~ 1,
    과정구분 == '대학원과정' ~ 2),
    졸업구분_node = case_when(
      졸업구분 == '취업' ~ 3,
      졸업구분 == '진학' ~ 4,
      졸업구분 == '취업불가' ~ 5,
      졸업구분 == '외국인' ~ 6,
      졸업구분 == '제외인정' ~ 7,
      졸업구분 == '기타' ~ 8,
      졸업구분 == '미상' ~ 9)
  ) |>
  arrange(과정구분_node, 졸업구분_node)

###############################################################################################
## 왼쪽 노드로 사용할 변량을 from에 저장
from <- unique(as.character(df_sankey$과정구분))

## 오른쪽 노드로 사용할 변량을 to에 저장
to <- unique(as.character(df_sankey$졸업구분))

## 전체 노드 벡터 생성
node <- c(from, to)

###############################################################################################
## sankey 트레이스 생성
df_sankey |> plot_ly(
  type = "sankey", orientation = "h",
  node = list(
    label = node,
    color = c(rep('lightblue', 3), rep('darkblue', 7)),
    pad = 15, thickness = 20,
    line = list(color = "black", width = 0.5)),
  link = list(
    source = ~과정구분_node,
    target = ~졸업구분_node,
    value = ~학생수)) |>
  layout(title = '대학과정별 졸업자의 졸업 후 진로',
         margin = margins_R)

###############################################################################################
## chap 10. 지수와 지도의 시각화
###############################################################################################
## indicator 트레이스를 위한 데이터 전처리
number_KOR <- total_deaths_5_nations_by_day |>
  filter(date == max(date), iso_code == 'KOR') |>
  select(total_deaths_per_million) |> pull()

fig <- total_deaths_5_nations_by_day |>
  plot_ly() |>
  ## scatter 트레이스 생성
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  ## layout의 제목, 축제목, 여백 속성 설정
  layout(title = list(text = '코로나19 사망자수 추세', pad = list(b = 5)),
         xaxis = list(title = ''),
         yaxis = list(title = '10만명당 사망자수 누계', domain = c(0, 0.8)),
         margin = margins_R)

## number 모드의 indicator 트레이스 추가
fig |> add_trace(type = 'indicator', mode = 'number', value = number_KOR,
                 title = list(text = paste0('<b>한국 코로나 사망자(10만명당)</b>\n',
                                            year(max(total_deaths_5_nations_by_day$date)), '년', month(max(total_deaths_5_nations_by_day$date)), '월', day(max(total_deaths_5_nations_by_day$date)), '일'),
                              font = list(family = '나눔고딕', size = 15)
                 ),
                 ## number 속성 설정
                 number = list(font = list(family = '나눔고딕', size = 15),
                               suffix = '명'),
                 domain = list(x = c(0.4, 0.6), y = c(0.8, 0.9)))

###############################################################################################
number1_KOR <- total_deaths_5_nations_by_day |>
  filter(date == max(date)-1, iso_code == 'KOR') |>
  select(total_deaths_per_million) |> pull()

fig <- total_deaths_5_nations_by_day |> plot_ly() |>
  ## scatter 트레이스 생성
  add_trace(type = 'scatter', mode = 'lines',
            x = ~date, y = ~total_deaths_per_million ,
            linetype = ~location, connectgaps = T) |>
  ## layout의 제목, 축제목, 여백 속성 설정
  layout(title = list(text = '코로나19 사망자수 추세', pad = list(b = 5)),
         xaxis = list(title = ''),
         yaxis = list(title = '10만명당 사망자수 누계', domain = c(0, 0.8)),
         margin = margins_R)
## number+delta 모드의 indicator 트레이스 추가
fig |> add_trace(type = 'indicator', mode = 'number+delta', value = number_KOR,
                 title = list(text = paste0('<b>한국 코로나 사망자(10만명당)</b>\n',
                                            year(max(total_deaths_5_nations_by_day$date)), '년', month(max(total_deaths_5_nations_by_day$date)), '월', day(max(total_deaths_5_nations_by_day$date)), '일'),
                              font = list(family = '나눔고딕', size = 15)),
                 number = list(font = list(family = '나눔고딕', size = 15),
                               suffix = '명'),
                 ## delta 속성 설정
                 delta = list(reference = number1_KOR, position = 'right',
                              increasing = list(color = 'red'),
                              decreasing = list(color = 'blue'),
                              font = list(family = '나눔고딕', size = 10)),
                 domain = list(x = c(0.4, 0.6), y = c(0.8, 0.9)))

###############################################################################################
## 게이지 indicator 트레이스를 위한 데이터 전처리
max_deaths_per_million_by_day <- total_deaths_5_nations_by_day |> group_by(location) |>
  summarise(최대사망자 = max(new_deaths_per_million, na.rm = TRUE))

deaths_per_million_in_lateast <- total_deaths_5_nations_by_day |> group_by(location) |>
  filter(is.na(new_deaths_per_million) == FALSE) |>
  filter(date == max(date)) |>
  select(iso_code, date, new_deaths_per_million)

df_gauge <- left_join(max_deaths_per_million_by_day, deaths_per_million_in_lateast, by = 'location') |> arrange(location)

## 한국 게이지 인디케이터 생성
fig_gauge <- df_gauge |> plot_ly() |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[3, 1]),
            domain = list(row = 1, column = 1), value = pull(df_gauge[3, 5]),
            gauge = list(axis = list(
              range = list(NULL, pull(df_gauge[3, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[3, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[3, 2])*1.2*0.5, pull(df_gauge[3, 2])*1.2*0.75),
                     color = "darkgray"),
                list(range = c(pull(df_gauge[3, 2])*1.2*0.75, pull(df_gauge[3, 2])*1.2), color
                     = "gray")),
              threshold = list(line = list(color = 'white'),
                               value = pull(df_gauge[3, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 프랑스 게이지 인디케이터 생성
fig_gauge <- fig_gauge |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[1, 1]),
            domain = list(row = 0, column = 0), value = pull(df_gauge[1, 5]),
            gauge = list(axis = list(
              range = list(NULL, pull(df_gauge[1, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[1, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[1, 2])*1.2*0.5, pull(df_gauge[1, 2])*1.2*0.75),
                     color = "darkgray"),
                list(range = c(pull(df_gauge[1, 2])*1.2*0.75, pull(df_gauge[1, 2])*1.2),
                     color = "gray")),
              threshold = list(line = list(color = 'white'),
                               value = pull(df_gauge[1, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 일본 게이지 인디케이터 생성
fig_gauge <- fig_gauge |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[2, 1]),
            domain = list(row = 0, column = 2), value = pull(df_gauge[2, 5]),
            gauge = list(axis = list(
              range = list(NULL, pull(df_gauge[2, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[2, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[2, 2])*1.2*0.5, pull(df_gauge[2, 2])*1.2*0.75),
                     color = "darkgray"),
                list(range = c(pull(df_gauge[2, 2])*1.2*0.75, pull(df_gauge[2, 2])*1.2),
                     color = "gray")),
              threshold = list(line = list(color = 'white'),
                               value = pull(df_gauge[2, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 영국 게이지 인디케이터 생성
fig_gauge <- fig_gauge |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[4, 1]),
            domain = list(row = 2, column = 0), value = pull(df_gauge[4, 5]),
            gauge = list(axis = list(
              range = list(NULL, pull(df_gauge[4, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[4, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[4, 2])*1.2*0.5, pull(df_gauge[4, 2])*1.2*0.75),
                     color = "darkgray"),
                list(range = c(pull(df_gauge[4, 2])*1.2*0.75, pull(df_gauge[4, 2])*1.2),
                     color = "gray")),
              threshold = list(line = list(color = 'white'),
                               value = pull(df_gauge[4, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 미국 게이지 인디케이터 생성
fig_gauge <- fig_gauge |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[5, 1]),
            domain = list(row = 2, column = 2), value = pull(df_gauge[5, 5]),
            gauge = list(axis = list(
              range = list(NULL, pull(df_gauge[5, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[5, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[5, 2])*1.2*0.5, pull(df_gauge[5, 2])*1.2*0.75),
                     color = "darkgray"),
                list(range = c(pull(df_gauge[5, 2])*1.2*0.75, pull(df_gauge[5, 2])*1.2),
                     color = "gray")),
              threshold = list(line = list(color = 'white'),
                               value = pull(df_gauge[5, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

fig_gauge |> layout(grid=list(rows=3, columns=3),
                    margin = margins_R,
                    title = '10만명당 사망자수(최근 공식발표 기준)')

###############################################################################################
## 한국 불릿 인디케이터 생성
fig_bullet <- df_gauge |> plot_ly() |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[3, 1]),
            domain = list(x = c(0.3,0.8), y = c(0.82, 0.9)),
            value = pull(df_gauge[3, 5]),
            gauge = list(axis = list(
              range = list(NULL, pull(df_gauge[3, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[3, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[3, 2])*1.2*0.5, pull(df_gauge[3, 2])*1.2*0.75), color = "darkgray"),
                list(range = c(pull(df_gauge[3, 2])*1.2*0.75, pull(df_gauge[3, 2])*1.2), color = "gray")),
              shape = "bullet",
              threshold = list(
                line = list(color = 'white'), value = pull(df_gauge[3, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 프랑스 불릿 인디케이터 생성
fig_bullet <- fig_bullet |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[1, 1]),
            domain = list(x = c(0.3,0.8), y = c(0.62, 0.7)),
            value = pull(df_gauge[1, 5]),
            gauge = list(axis = list(
              shape = "bullet",
              range = list(NULL, pull(df_gauge[1, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[1, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[1, 2])*1.2*0.5, pull(df_gauge[1, 2])*1.2*0.75), color = "darkgray"),
                list(range = c(pull(df_gauge[1, 2])*1.2*0.75, pull(df_gauge[1, 2])*1.2), color = "gray")),
              shape = "bullet",
              threshold = list(
                line = list(color = 'white'), value = pull(df_gauge[1, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 일본 불릿 인디케이터 생성
fig_bullet <- fig_bullet |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[2, 1]),
            domain = list(x = c(0.3,0.8), y = c(0.42, 0.5)),
            value = pull(df_gauge[2, 5]),
            gauge = list(axis = list(
              shape = "bullet",
              range = list(NULL, pull(df_gauge[2, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[2, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[2, 2])*1.2*0.5, pull(df_gauge[2, 2])*1.2*0.75), color = "darkgray"),
                list(range = c(pull(df_gauge[2, 2])*1.2*0.75, pull(df_gauge[2, 2])*1.2), color = "gray")),
              shape = "bullet",
              threshold = list(
                line = list(color = 'white'), value = pull(df_gauge[2, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 영국 불릿 인디케이터 생성
fig_bullet <- fig_bullet |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[4, 1]),
            domain = list(x = c(0.3,0.8), y = c(0.22, 0.3)),
            value = pull(df_gauge[4, 5]),
            gauge = list(axis = list(
              shape = "bullet",
              range = list(NULL, pull(df_gauge[4, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[4, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[4, 2])*1.2*0.5, pull(df_gauge[4, 2])*1.2*0.75), color = "darkgray"),
                list(range = c(pull(df_gauge[4, 2])*1.2*0.75, pull(df_gauge[4, 2])*1.2), color = "gray")),
              shape = "bullet",
              threshold = list(
                line = list(color = 'white'), value = pull(df_gauge[4, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

## 미국 불릿 인디케이터 생성
fig_bullet <- fig_bullet |>
  add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[5, 1]),
            domain = list(x = c(0.3,0.8), y = c(0.02, 0.1)),
            value = pull(df_gauge[5, 5]),
            gauge = list(axis = list(
              shape = "bullet",
              range = list(NULL, pull(df_gauge[5, 2])*1.2)),
              steps = list(
                list(range = c(0, pull(df_gauge[5, 2])*1.2*0.5), color = "lightgray"),
                list(range = c(pull(df_gauge[5, 2])*1.2*0.5, pull(df_gauge[5, 2])*1.2*0.75), color = "darkgray"),
                list(range = c(pull(df_gauge[5, 2])*1.2*0.75, pull(df_gauge[5, 2])*1.2), color = "gray")),
              shape = "bullet",
              threshold = list(
                line = list(color = 'white'), value = pull(df_gauge[5, 2])),
              bar = list(color = "darkblue")),
            number = list(suffix = '명'))

fig_bullet |> layout(margin = margins_R,
                     title = '10만명당 사망자수(최근 공식발표 기준)')

###############################################################################################
plot_ly() |>
  ## scattergoe 트레이스 생성
  add_trace(type = 'scattergeo') |>
  layout(geo = list(resolution=50,
                    showcoastlines=TRUE, coastlinecolor='RebeccaPurple',
                    showland=TRUE, landcolor='LightGray',
                    showocean=TRUE, oceancolor='LightBlue',
                    showlakes=TRUE, lakecolor='white',
                    showrivers=TRUE, rivercolor='Blue'),
         margin = list(r = 0, l = 0, t = 0, b = 0))

###############################################################################################
plot_ly() |>
  add_trace(type = 'scattergeo') |>
  layout(geo = list(resolution=50, scope = 'asia',
                    showcountries=TRUE, countrycolor="black"),
         margin = list(r = 0, l = 0, t = 0, b = 0))

###############################################################################################
## 지도를 위한 패키지 로딩
if (!require(raster)) {
  install.packages('raster')
  library(raster) }
if (!require(sf)) {
  install.packages('sf')
  library(sf) }

#### 충원율 데이터
df_충원율 <- read_excel('./고등 주요 01-시도별 신입생 충원율(2010-2022)_220825y.xlsx',
                     sheet = 'Sheet1', skip = 7, col_names = FALSE,
                     col_types = c(rep('text', 2), rep('numeric', 12)))

df_충원율 <- df_충원율 |> dplyr::select(1, 2, 3, 4, 5)

## df_입학자의 열이름을 적절한 이름으로 설정
colnames(df_충원율) <- c('연도', '지역', '정원내모집인원', '정원내입학생수', '신입생충원율')

## 지형 데이터와 매칭을 위한 열 생성
df_충원율 <- df_충원율 |> filter(연도 == '2022', 지역 != '전국') |>
  mutate(id = case_when(
    지역 == '강원' ~ 'KR.KW', 지역 == '경기' ~ 'KR.KG',
    지역 == '경남' ~ 'KR.KN', 지역 == '경북' ~ 'KR.KB',
    지역 == '광주' ~ 'KR.KJ', 지역 == '대구' ~ 'KR.TG',
    지역 == '대전' ~ 'KR.TJ', 지역 == '부산' ~ 'KR.PU',
    지역 == '서울' ~ 'KR.SO', 지역 == '세종' ~ 'KR.SJ',
    지역 == '울산' ~ 'KR.UL', 지역 == '인천' ~ 'KR.IN',
    지역 == '전남' ~ 'KR.CN', 지역 == '전북' ~ 'KR.CB',
    지역 == '제주' ~ 'KR.CJ', 지역 == '충남' ~ 'KR.GN',
    지역 == '충북' ~ 'KR.GB'))

## sf 포맷으로 한국 지형 데이터를 가져옴
map_data <- getData("GADM", country = "KOR", level = 1, type = "sf")

## old crs 경고를 없애기 위해 사용
st_crs(map_data) <- st_crs(map_data)

## 조인된 데이터를 sf 클래스로 변환
plot_dat <- left_join(map_data, df_충원율, by = c("HASC_1" = "id")) %>%
  st_as_sf()

plot_ly(plot_dat) %>%
  add_sf(type = "scatter",
         split = ~지역, color = ~신입생충원율,
         showlegend = F, colors = "Blues",
         text = ~paste0(지역, "\n", round(신입생충원율, 2), '%'), ## 호버에 표시될 텍스트 설정
         hoveron = "fills", hoverinfo = "text") %>%
  layout(title = '22년 전국 대학 신입생 충원율',
         margin = margins_R)

###############################################################################################
## 맵박스 토큰 설정
Sys.setenv('MAPBOX_TOKEN' = '')

###############################################################################################
## 대학의 위경도 데이터 불러들임
df_univ <- read_excel("./university.xlsx",
                      col_types = c('text', 'numeric', 'numeric'))

plot_dat_seoul <- plot_dat |> filter(GID_1 == 'KOR.16_1')

plot_mapbox(plot_dat_seoul) |>
  add_trace(data = df_univ, type = 'scattermapbox', mode = 'markers+text',
            x = ~lon, y = ~lat,
            marker = list(size = 10, symbol = 'marker'),
            text = ~학교명, textposition = 'top center',
            textfont = list(color = 'blue')) |>
  layout(title = '서울지역 주요 대학',
         autosize=TRUE, hovermode='closest',
         mapbox=list(
           bearing=0, center=list(lon=126.98, lat=37.56),
           pitch=0, zoom=10, style="light"),
         margin = margins_R,
         showlegend = FALSE)

###############################################################################################

###############################################################################################

