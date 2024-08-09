if(!require(shiny)) {
  install.packages('shiny')
  library(shiny) }

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

if(!require(plotly)) {        ## 플로틀리 로딩이 안 되면
  install.packages('plotly')  ## 플로틀리  패키지 설치
  library(plotly)             ## 플로틀리 패키지 로딩
}

## 1. covid19 원본 데이터셋 로딩
## covid19 데이터 로딩(파일을 다운로드 받은 경우)
df_covid19 <- read_csv(file = "D:/R/data/Rnpy/owid-covid-data.csv",
                       col_types = cols(date = col_date(format = "%Y-%m-%d")
                       )
)
## covid19 데이터 로딩(온라인에서 바로 로딩할 경우)
# df_covid19 <- read_csv(file = "https://covid.ourworldindata.org/data/owid-covid-data.csv",
#                             col_types = cols(Date = col_date(format = "%Y-%m-%d")
#                                              )
#                             )
## 2. 전체 데이터셋 중 최근 100일간의 데이터를 필터링한 df_covid19_100 생성
df_covid19_100 <- df_covid19 |> 
  ## 한국 데이터와 각 대륙별 데이터만을 필터링
  filter(iso_code %in% c('KOR', 'OWID_ASI', 'OWID_EUR', 'OWID_OCE', 'OWID_NAM', 'OWID_SAM', 'OWID_AFR')) |>
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
  mutate(location = fct_relevel(location, '한국', '아시아', '유럽', '북미', '남미', '아프리카', '오세아니아')) |>
  ## 날짜로 정렬
  arrange(date)


## 3. df_covid19_100을 한국과 각 대륙별 열로 배치한 넓은 형태의 데이터프레임으로 변환
df_covid19_100_wide <- df_covid19_100 |>
  ## 날짜, 국가명, 확진자와, 백신접종완료자 데이터만 선택
  select(date, location, new_cases, people_fully_vaccinated_per_hundred) |>
  ## 열 이름을 적절히 변경
  rename('date' = 'date', '확진자' = 'new_cases', '백신접종완료자' = 'people_fully_vaccinated_per_hundred') |>
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

##  dash 앱의 구성을 위한 데이터 전처리
total_deaths_5_nations_by_day <- df_covid19 |> 
  filter((iso_code %in% c('KOR', 'USA', 'JPN', 'GBR', 'FRA'))) |>
  filter(!is.na(total_deaths_per_million))

last_day = max(distinct(total_deaths_5_nations_by_day, date) |> pull())

##  indicator 트레이스에서 사용할 각각의 국가별 최대 사망자 추출
max_deaths_per_million_by_day <- total_deaths_5_nations_by_day |> group_by(location) |>
  summarise(최대사망자 = max(new_deaths_per_million, na.rm = TRUE))

##  indicator 트레이스에서 사용할 십만명당 사망자수 추출
deaths_per_million_in_lateast <- total_deaths_5_nations_by_day |> group_by(location) |>
  filter(is.na(new_deaths_per_million) == FALSE) |>
  filter(date == max(date)) |>
  select(iso_code, date, new_deaths_per_million)

##  indicator 트레이스에서 사용할 데이터 전처리
df_gauge <- left_join(max_deaths_per_million_by_day, deaths_per_million_in_lateast, by = 'location') |> arrange(location)

###############################################################################################
## APPENDIX A R과 파이썬을 사용한 대시보드 만들기
###############################################################################################
if(!require(shiny)) {
  install.packages('shiny')
  library(shiny)
}

###############################################################################################
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(

    ## ui 객체 정의 부분

)

# Define server logic required to draw a histogram
server <- function(input, output) {

## server 객체 정의 부분

}

# Run the application
shinyApp(ui = ui, server = server) ## R Shiny 애플리케이션 실행 부분

###############################################################################################
ui <- fluidPage(
  fluidRow(column(width = 4),
       column(width = 2, offset = 3)),
  fluidRow(column(width = 12))
)

print(ui)

<div class="container-fluid">
  <div class="row">
    <div class="col-sm-4"></div>
    <div class="col-sm-2 offset-md-3 col-sm-offset-3"></div>
  </div>
  <div class="row">
    <div class="col-sm-12"></div>
  </div>
</div>

###############################################################################################
# Define server logic ----
server <- function(input, output)
  react <- reactive({ ## 리액티비티 컨덕터 정의
    input$n * 2
  })

  output$hist <- renderPlot({
    hist(rnorm(react())) ## 리책티비티 컨덕터 사용
  })
}

###############################################################################################
if(!require(shiny)) {
  install.packages('shiny')
  library(shiny) }

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

if(!require(plotly)) {        ## 플로틀리 로딩이 안 되면
  install.packages('plotly')  ## 플로틀리 패키지 설치
  library(plotly)             ## 플로틀리 패키지 로딩
}

## 1. covid19 원본 데이터셋 로딩
## covid19 데이터 로딩(파일을 다운로드 받은 경우)
df_covid19 <- read_csv(file = "D:/R/data/Rnpy/owid-covid-data.csv",
                       col_types = cols(date = col_date(format = "%Y-%m-%d")
                       )
)

## covid19 데이터 로딩(온라인에서 바로 로딩할 경우)
# df_covid19 <- read_csv(file = "https://covid.ourworldindata.org/data/owid-covid-data.csv",
#                             col_types = cols(Date = col_date(format = "%Y-%m-%d")
#                                              )
#                             )

## 2. 전체 데이터셋 중 최근 100일간의 데이터를 필터링한 df_covid19_100 생성
df_covid19_100 <- df_covid19 |> 
  ## 한국 데이터와 각 대륙별 데이터만을 필터링
  filter(iso_code %in% c('KOR', 'OWID_ASI', 'OWID_EUR', 'OWID_OCE', 'OWID_NAM', 'OWID_SAM', 'OWID_AFR')) |>
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
  mutate(location = fct_relevel(location, '한국', '아시아', '유럽', '북미', '남미', '아프리카', '오세아니아')) |>
  ## 날짜로 정렬
  arrange(date)


## 3. df_covid19_100을 한국과 각 대륙별 열로 배치한 넓은 형태의 데이터프레임으로 변환
df_covid19_100_wide <- df_covid19_100 |>
  ## 날짜, 국가명, 확진자와, 백신접종완료자 데이터만 선택
  select(date, location, new_cases, people_fully_vaccinated_per_hundred) |>
  ## 열 이름을 적절히 변경
  rename('date' = 'date', '확진자' = 'new_cases', '백신접종완료자' = 'people_fully_vaccinated_per_hundred') |>
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

##  dash 앱의 구성을 위한 데이터 전처리
total_deaths_5_nations_by_day <- df_covid19 |> 
  filter((iso_code %in% c('KOR', 'USA', 'JPN', 'GBR', 'FRA'))) |>
  filter(!is.na(total_deaths_per_million))

last_day = max(distinct(total_deaths_5_nations_by_day, date) |> pull())

##  indicator 트레이스에서 사용할 각각의 국가별 최대 사망자 추출
max_deaths_per_million_by_day <- total_deaths_5_nations_by_day |> group_by(location) |>
  summarise(최대사망자 = max(new_deaths_per_million, na.rm = TRUE))

##  indicator 트레이스에서 사용할 십만명당 사망자수 추출
deaths_per_million_in_lateast <- total_deaths_5_nations_by_day |> group_by(location) |>
  filter(is.na(new_deaths_per_million) == FALSE) |>
  filter(date == max(date)) |>
  select(iso_code, date, new_deaths_per_million)

##  indicator 트레이스에서 사용할 데이터 전처리
df_gauge <- left_join(max_deaths_per_million_by_day, deaths_per_million_in_lateast, by = 'location') |> arrange(location)

###############################################################################################
ui <- fluidPage(
  fluidRow(
    column(12,
           titlePanel(h1("코로나19 사망자수 추세", align = "center"))
    )    ##  첫 번째 행은 길이 12의 단일 컬럼
  ),
  fluidRow(
    column(2, 
           dateInput("date1", "Date:", value = last_day, language = 'ko', autoclose = FALSE)
           ), 
    column(10, 
           fluidRow(
             column(10, plotly::plotlyOutput('plot_trendy_names'), offset = 1)
           ), 
           fluidRow(
             column(1),
             column(2, plotly::plotlyOutput('plot_trendy_kor')),
             column(2, plotly::plotlyOutput('plot_trendy_fra')),
             column(2, plotly::plotlyOutput('plot_trendy_jpn')),
             column(2, plotly::plotlyOutput('plot_trendy_gbr')),
             column(2, plotly::plotlyOutput('plot_trendy_usa')),
             column(1)
           )
           )
  )
)

###############################################################################################
server = function(input, output) {
  
  dataInput <- reactive({
    deaths_per_million_update <- total_deaths_5_nations_by_day |> 
      filter(is.na(new_deaths_per_million) == FALSE) |>
      filter(date == input$date1) |>
      select(location, new_deaths_per_million) |> arrange(location)
  })
  
  output$plot_trendy_names <- plotly::renderPlotly({
    total_deaths_5_nations_by_day |>
      plot_ly() |>
      add_trace(type = 'scatter', mode = 'lines', 
                x = ~date, y = ~total_deaths_per_million , linetype = ~location, connectgaps = T, 
                color = ~location) |>
      add_annotations( 
        x =~ (total_deaths_5_nations_by_day |> filter(date == max(date)) |> select(date) |> pull()), 
        y = ~(total_deaths_5_nations_by_day |> filter(date == max(date)) |> select(total_deaths_per_million) |> pull()),
        text = ~(total_deaths_5_nations_by_day |> filter(date == max(date)) |> select(location) |> pull()), 
        textposition = 'middle right', xanchor = 'left', showarrow = FALSE
      ) |>
      layout(title = '코로나 19 사망자수 추세', 
             xaxis = list(title = '', range = c('2020-02-15', format(last_day, format="%Y-%m-%d"))), 
             yaxis = list(title = '10만명당 사망자수 누계'), 
             margin = margins_R,
             showlegend = FALSE) |> 
      layout(shapes = list(type = 'line', y0 = 0, 
                           y1 = max(total_deaths_5_nations_by_day$total_deaths_per_million), 
                           yref = "y", x0 = input$date1, x1 = input$date1,
                           line = list(color = 'black', dash="dot")))
  })
  output$plot_trendy_kor <- plotly::renderPlotly({
    df_gauge |> plot_ly() |>
      add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[3, 1]),
                value = pull(dataInput()[3, 2]), 
                gauge = list(axis = list(
                  range = list(NULL, pull(df_gauge[3, 2])*1.2)),
                  steps = list(
                    list(range = c(0, pull(df_gauge[3, 2])*1.2*0.5), color = "lightgray"),
                    list(range = c(pull(df_gauge[3, 2])*1.2*0.5, pull(df_gauge[3, 2])*1.2*0.75), color = "darkgray"),
                    list(range = c(pull(df_gauge[3, 2])*1.2*0.75, pull(df_gauge[3, 2])*1.2), color = "gray")),
                  threshold = list(line = list(color = 'white'),
                                   value = pull(df_gauge[3, 2])), 
                  bar = list(color = "darkblue")), 
                number = list(suffix = '명'), 
                domain = list(x = c(0, 1), y = c(0.5, 1))) 
  })
  
  output$plot_trendy_fra <- plotly::renderPlotly({
    df_gauge |> plot_ly() |>
      add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[1, 1]),
                value = pull(dataInput()[1, 2]), 
                gauge = list(axis = list(
                  range = list(NULL, pull(df_gauge[1, 2])*1.2)),
                  steps = list(
                    list(range = c(0, pull(df_gauge[1, 2])*1.2*0.5), color = "lightgray"),
                    list(range = c(pull(df_gauge[1, 2])*1.2*0.5, pull(df_gauge[1, 2])*1.2*0.75), color = "darkgray"),
                    list(range = c(pull(df_gauge[1, 2])*1.2*0.75, pull(df_gauge[1, 2])*1.2), color = "gray")),
                  threshold = list(line = list(color = 'white'),
                                   value = pull(df_gauge[1, 2])), 
                  bar = list(color = "darkblue")), 
                number = list(suffix = '명'), 
                domain = list(x = c(0, 1), y = c(0.5, 1)))
  })
  
  output$plot_trendy_jpn <- plotly::renderPlotly({
    df_gauge |> plot_ly() |>
      add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[2, 1]),
                value = pull(dataInput()[2, 2]), 
                gauge = list(axis = list(
                  range = list(NULL, pull(df_gauge[2, 2])*1.2)),
                  steps = list(
                    list(range = c(0, pull(df_gauge[2, 2])*1.2*0.5), color = "lightgray"),
                    list(range = c(pull(df_gauge[2, 2])*1.2*0.5, pull(df_gauge[2, 2])*1.2*0.75), color = "darkgray"),
                    list(range = c(pull(df_gauge[2, 2])*1.2*0.75, pull(df_gauge[2, 2])*1.2), color = "gray")),
                  threshold = list(line = list(color = 'white'),
                                   value = pull(df_gauge[2, 2])), 
                  bar = list(color = "darkblue")), 
                number = list(suffix = '명'), 
                domain = list(x = c(0, 1), y = c(0.5, 1)))
  })
  
  output$plot_trendy_gbr <- plotly::renderPlotly({
    df_gauge |> plot_ly() |>
      add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[4, 1]),
                value = pull(dataInput()[4, 2]), 
                gauge = list(axis = list(
                  range = list(NULL, pull(df_gauge[4, 2])*1.2)),
                  steps = list(
                    list(range = c(0, pull(df_gauge[4, 2])*1.2*0.5), color = "lightgray"),
                    list(range = c(pull(df_gauge[4, 2])*1.2*0.5, pull(df_gauge[4, 2])*1.2*0.75), color = "darkgray"),
                    list(range = c(pull(df_gauge[4, 2])*1.2*0.75, pull(df_gauge[4, 2])*1.2), color = "gray")),
                  threshold = list(line = list(color = 'white'),
                                   value = pull(df_gauge[4, 2])), 
                  bar = list(color = "darkblue")), 
                number = list(suffix = '명'), 
                domain = list(x = c(0, 1), y = c(0.5, 1)))
  })
  output$plot_trendy_usa <- plotly::renderPlotly({
    df_gauge |> plot_ly() |>
      add_trace(type = 'indicator', mode = "gauge+number", title = pull(df_gauge[5, 1]),
                value = pull(dataInput()[5, 2]), 
                gauge = list(axis = list(
                  range = list(NULL, pull(df_gauge[5, 2])*1.2)),
                  steps = list(
                    list(range = c(0, pull(df_gauge[5, 2])*1.2*0.5), color = "lightgray"),
                    list(range = c(pull(df_gauge[5, 2])*1.2*0.5, pull(df_gauge[5, 2])*1.2*0.75), color = "darkgray"),
                    list(range = c(pull(df_gauge[5, 2])*1.2*0.75, pull(df_gauge[5, 2])*1.2), color = "gray")),
                  threshold = list(line = list(color = 'white'),
                                   value = pull(df_gauge[5, 2])), 
                  bar = list(color = "darkblue")), 
                number = list(suffix = '명'), 
                domain = list(x = c(0, 1), y = c(0.5, 1)))
  })

}

###############################################################################################
shinyApp(ui, server)

###############################################################################################