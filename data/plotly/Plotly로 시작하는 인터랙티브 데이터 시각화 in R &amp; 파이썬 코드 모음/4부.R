###############################################################################################
## chap 2. plotly 시각화 만들기
###############################################################################################
## R code
## 데이터 전처리를 위한 패키지 설치 및 로딩
if(!require(tidyverse)) {
  install.packages('tidyverse')
  library(tidyverse) }
if(!require(readxl)) {
  install.packages('readxl')
  library(readxl) }
if(!require(readr)) {
  install.packages('readr')
  library(readr) }
if(!require(lubridate)) {
  install.packages('lubridate')
  library(lubridate) }
## 1. covid19 원본 데이터셋 로딩
## covid19 데이터 로딩(파일을 다운로드 받은 경우)
df_covid19 <- read_csv(file = "./owid-covid-data.csv",
                       col_types = cols(date = col_date(format = "%Y-%m-%d")
                       )
)
## covid19 데이터 로딩(온라인에서 바로 로딩할 경우)
# df_covid19 <- read_csv(file = "https://covid.ourworldindata.org/data/owid-covid-data.csv",
# col_types = cols(Date = col_date(format = "%Y-%m-%d")
# )
# )
## 2. 전체 데이터셋 중 최근 100일간의 데이터를 필터링한 df_covid19_100 생성
df_covid19_100 <- df_covid19 |>
  ## 한국 데이터와 각 대륙별 데이터만을 필터링
  filter(iso_code %in% c('KOR', 'OWID_ASI', 'OWID_EUR', 'OWID_OCE', 'OWID_NAM', 'OWID_SAM',
                         'OWID_AFR')) |>
  ## 읽은 데이터의 마지막 데이터에서 100일 전 데이터까지 필터링
  filter(date >= max(date) - 100) |>
  ## 국가명을 한글로 변환
  mutate(location = case_when(
    location == 'South Korea' ~ '한국',
    location == 'Asia' ~ '아시아',
    location == 'Europe' ~ '유럽',
    location == 'Oceania' ~ '오세아니아',
    location == 'North America' ~ '북미',
    location == 'South America' ~ '남미',
    location == 'Africa' ~ '아프리카')) |>
  ## 국가 이름의 순서를 설정
  mutate(location = fct_relevel(location, '한국', '아시아', '유럽', '북미', '남미', '아프리카',
                                '오세아니아')) |>
  ## 날짜로 정렬
  arrange(date)
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
## chap 11. 시각화 컨트롤
## 연도별 충원율 데이터를 불러들이고 전처리
df_충원율_button <- read_excel(
  '데이터저장경로/고등 주요 01-시도별 신입생 충원율(2010-2022)_220825y.xlsx',
  sheet = 'Sheet1', skip = 7, col_names = FALSE, 
  col_types = c(rep('text', 2), rep('numeric', 12)))

df_충원율_button <- df_충원율_button |> dplyr::select(1, 2, 5)

colnames(df_충원율_button) <- c('연도', '지역', '신입생충원율')

df_충원율_button <- df_충원율_button |> 
  pivot_wider(names_from = '연도', values_from = '신입생충원율')

df_충원율_button <- as.data.frame(df_충원율_button)

###############################################################################################
fig <- df_충원율_button |>
  plot_ly() |>
  ## 데이터가 표시되는 bar 트레이스 생성
  add_trace(type = 'bar', x = ~지역,
            y = ~`2022`, text = ~`2022`,
            texttemplate = '%{text:.1f}%', textposition = 'outside')

## 버튼 제목이 표시되는 주석 레이어 생성
fig <- fig |> add_annotations(x = -0.1, y = 0.85, text = '<b>연도</b>',
                              xanchor = 'center', yanchor = 'middle',
                              yref='paper', xref='paper', showarrow=FALSE )

## 버튼 생성
fig <- fig %>% layout(
  title = "2022년 지역별 충원율",
  xaxis = list(domain = c(0.1, 1), categoryorder = "total descending"),
  yaxis = list(title = "충원율(%)"),
  updatemenus = list( ## updatemenus의 할당을 위한 리스트 정의
    list( ## updatemenus의 버튼 그룹 리스트 설정
      type = "buttons", y = 0.8,
      buttons = list( ## 버튼 그룹에 생성되는 다섯 개의 버튼 설정
        list( ## 첫 번째 버튼 정의
          method = "restyle",
          args = list( ## 첫 번째 버튼의 args 설정
            list(
              y = list(df_충원율_button$`2018`),
              text = list(df_충원율_button$`2018`)
            )
          ),
          label = "2018년"
        ),
        list( ## 두 번째 버튼 정의
          method = "restyle",
          args = list( ## 두 번째 버튼의 args 설정
            list(
              y = list(df_충원율_button$`2019`),
              text = list(df_충원율_button$`2019`)
            )
          ),
          label = "2019년"
        ),
        list( ## 세 번째 버튼 정의
          method = "restyle",
          args = list( ## 세 번째 버튼의 args 설정
            list(
              y = list(df_충원율_button$`2020`),
              text = list(df_충원율_button$`2020`)
            )
          ),
          label = "2020년"
        ),
        list( ## 네 번째 버튼 정의
          method = "restyle",
          args = list( ## 네 번째 버튼의 args 설정
            list(
              y = list(df_충원율_button$`2021`),
              text = list(df_충원율_button$`2021`)
            )
          ),
          label = "2021년"),
        list( ## 댜섯 번째 버튼 정의
          method = "restyle",
          args = list( ## 다섯 번째 버튼의 args 설정
            list(
              y = list(df_충원율_button$`2022`),
              text = list(df_충원율_button$`2022`)
            )
          ),
          label = "2022년")
      )
    )
  ),
  margin = margins_R)

fig

###############################################################################################
fig <- df_충원율_button |>
  plot_ly() |>
  add_trace(type = 'bar', x = ~지역, y = ~`2022`, text = ~`2022`,
            texttemplate = '%{text:.1f}%', textposition = 'outside')
fig <- fig |> add_annotations(x = -0.1, y = 0.85, text = '<b>연도</b>',
                              xanchor = 'center', yanchor = 'middle',
                              yref='paper', xref='paper', showarrow=FALSE )
fig <- fig %>% layout(
  title = "2022년 지역별 충원율",
  xaxis = list(domain = c(0.1, 1), categoryorder = "total descending"),
  yaxis = list(title = "충원율(%)"),
  updatemenus = list( ## updatemenus의 할당을 위한 리스트 정의
    list( ## updatemenus의 버튼 그룹 리스트 설정
      type = "buttons",
      y = 0.8,
      buttons = list( ## 버튼 그룹에 생성되는 다섯 개의 버튼 설정
        list(method = "relayout", ## 첫 번째 버튼 정의
             args = list(list(title.text='2018년 지역별 충원율')),
             ## 첫 번째 버튼의 args 설정
             label = "2018년"),
        list(method = "relayout", ## 두 번째 버튼의 args 설정
             args = list(list(title.text='2019년 지역별 충원율')),
             ## 두 번째 버튼의 args 설정
             label = "2019년"),
        list(method = "relayout", ## 세 번째 버튼의 args 설정
             args = list(list(title.text='2020년 지역별 충원율')),
             ## 세 번째 버튼의 args 설정
             label = "2020년"),
        list(method = "relayout", ## 네 번째 버튼의 args 설정
             args = list(list(title.text='2021년 지역별 충원율')),
             ## 네 번째 버튼의 args 설정
             label = "2021년"),
        list(method = "relayout", ## 다섯 번째 버튼의 args 설정
             args = list(list(title.text='2022년 지역별 충원율')),
             ## 다섯 번째 버튼의 args 설정
             label = "2022년")))
  ),
  margin = margins_R)

fig

###############################################################################################
fig <- df_충원율_button |>
  plot_ly() |>
  add_trace(type = 'bar', x = ~지역, y = ~`2022`, text = ~`2022`,
            texttemplate = '%{text:.1f}%', textposition = 'outside')

fig <- fig |> add_annotations(x = -0.1, y = 0.85, text = '<b>연도</b>',
                              xanchor = 'center', yanchor = 'middle',
                              yref='paper', xref='paper', showarrow=FALSE )

fig <- fig %>% layout(
  title = '2022년 지역별 충원율',
  xaxis = list(domain = c(0.1, 1), categoryorder = "total descending"),
  yaxis = list(title = "충원율(%)"),
  updatemenus = list( ## updatemenus의 할당을 위한 리스트 정의
    list( ## updatemenus의 버튼 그룹 리스트 설정
      type = "buttons",
      y = 0.8,
      buttons = list( ## 버튼 그룹에 생성되는 다섯 개의 버튼 설정
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2018`),
                              ## 첫 번째 버튼의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2018`)),
                         list(title.text='2018년 지역별 충원율')),
             ## 첫 번째 버튼의 layout 속성에 대한 args 설정
             label = "2018년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2019`),
                              ## 두 번째 버튼의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2019`)),
                         list(title.text='2019년지역별 충원율')),
             ## 두 번째 버튼의 layout 속성에 대한 args 설정
             label = "2019년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2020`),
                              ## 세 번째 버튼의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2020`)),
                         list(title.text='2020년 지역별 충원율')),
             ## 세 번째 버튼의 layout 속성에 대한 args 설정
             label = "2020년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2021`),
                              ## 네 번째 버튼의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2021`)),
                         list(title.text='2021년 지역별 충원율')),
             ## 네 번째 버튼의 layout 속성에 대한 args 설정
             label = "2021년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2022`),
                              ## 다섯 번째 버튼의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2022`)),
                         list(title.text='2022년 지역별 충원율')),
             ## 다섯 번째 버튼의 layout 속성에 대한 args 설정
             label = "2022년")))
  ),
  margin = margins_R)

fig


###############################################################################################
fig <- df_충원율_button |>
  plot_ly() |>
  add_trace(type = 'bar', x = ~지역, y = ~`2022`, text = ~`2022`,
            texttemplate = '%{text:.1f}%', textposition = 'outside')

fig <- fig |> add_annotations(x = -0.1, y = 0.85, text = '<b>연도</b>',
                              xanchor = 'center', yanchor = 'middle',
                              yref='paper', xref='paper', showarrow=FALSE )
fig <- fig %>% layout(
  title = '2022년 지역별 충원율',
  xaxis = list(domain = c(0.1, 1), categoryorder = "total descending"),
  yaxis = list(title = "충원율(%)"),
  updatemenus = list( ## updatemenus의 할당을 위한 리스트 정의
    list( ## updatemenus의 드롭다운 리스트 설정
      type = 'dropdown',
      y = 0.8,
      buttons = list( ## 드롭다운에 생성되는 다섯 개의 메뉴 설정
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2018`),
                              ## 첫 번째 메뉴의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2018`)),
                         list(title.text='2018년 지역별 충원율')),
             ## 첫 번째 메뉴의 layout 속성에 대한 args 설정
             label = "2018년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2019`),
                              ## 두 번째 메뉴의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2018`)),
                         list(title.text='2019년지역별 충원율')),
             ## 두 번째 메뉴의 layout 속성에 대한 args 설정
             label = "2019년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2020`),
                              ## 세 번째 메뉴의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2018`)),
                         ## 세 번째 메뉴의 layout 속성에 대한 args 설정
                         list(title.text='2020년 지역별 충원율')),
             label = "2020년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2021`),
                              ## 네 번째 메뉴의 data 속성에 대한 args 설정
                              text = list(df_충원율_button$`2018`)),
                         list(title.text='2021년 지역별 충원율')),
             ## 네 번째 메뉴의 layout 속성에 대한 args 설정
             label = "2021년"),
        list(method = "update",
             args = list(list(y = list(df_충원율_button$`2022`),
                              ## 다섯 번째 메뉴의 data 속성에 대한 args 설정
                              text = list(df_충원율$`2018`)),
                         list(title.text='2022년 지역별 충원율')),
             ## 다섯 번째 메뉴의 layout 속성에 대한 args 설정
             label = "2022년")))
  ),
  margin = margins_R)

fig

###############################################################################################
fig <- df_충원율_button |>
  plot_ly() |>
  add_trace(type = 'bar', x = ~지역,
            y = ~`2022`, text = ~paste0(sprintf('%.1f', df_충원율_button$`2022`), '%'),
            textposition = 'outside')

## 슬라이더 설정을 위한 steps 속성 설정
steps <- list(
  list(method = "update",
       args = list(list(y = list(df_충원율_button$`2018`),
                        text = list(paste0(sprintf('%.1f', df_충원율_button$`2018`),
                                           '%'))),
                   list(title.text='2018년 지역별 충원율')),
       label = "2018년", value = "1"),
  list(method = "update",
       args = list(list(y = list(df_충원율_button$`2019`),
                        text = list(paste0(sprintf('%.1f', df_충원율_button$`2019`),
                                           '%'))),
                   list(title.text='2019년지역별 충원율')),
       label = "2019년", value = "2"),
  list(method = "update",
       args = list(list(y = list(df_충원율_button$`2020`),
                        text = list(paste0(sprintf('%.1f', df_충원율_button$`2020`),
                                           '%'))),
                   list(title.text='2020년 지역별 충원율')),
       label = "2020년", value = "3"),
  list(method = "update",
       args = list(list(y = list(df_충원율_button$`2021`),
                        text = list(paste0(sprintf('%.1f', df_충원율_button$`2021`),
                                           '%'))),
                   list(title.text='2021년 지역별 충원율')),
       label = "2021년", value = "4"),
  list(method = "update",
       args = list(list(y = list(df_충원율_button$`2022`),
                        text = list(paste0(sprintf('%.1f', df_충원율_button$`2022`),
                                           '%'))),
                   list(title.text='2022년 지역별 충원율')),
       label = "2022년", value = "5")
)

fig <- fig %>% layout(
  title = '2022년 지역별 충원율',
  xaxis = list(categoryorder = "total descending"),
  yaxis = list(title = "충원율(%)"),
  sliders = list(
    list(
      active = 6, currentvalue = list(prefix = "연도: "),
      pad = list(t = 60),
      steps = steps)),
  margin = margins_R)

fig


###############################################################################################
## chap 13. Plotly 배포
###############################################################################################
fig <- df_취업률_500 |>
  ## X축은 졸업자수, Y축은 취업자수로 매핑한 Plotly 객체 생성
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'markers',
            x = ~졸업자수, y = ~취업자수)

export(fig, file = 'fig.png')

###############################################################################################
htmlwidgets::saveWidget(widget = fig, 'fig.html')

###############################################################################################
Sys.setenv("plotly_username"="차트 스튜디오의 사용자 이름")
Sys.setenv("plotly_api_key"="차트 스튜디오의 API Key값")

###############################################################################################
fig <- df_취업률_500 |>
  ## X축은 졸업자수, Y축은 취업자수로 매핑한 Plotly 객체 생성
  plot_ly() |>
  add_trace(type = 'scatter', mode = 'markers',
            x = ~졸업자수, y = ~취업자수)

  api_create(fig, filename = "업로드할 파일 이름")

###############################################################################################







