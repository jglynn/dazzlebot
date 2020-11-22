# Fireball Draw Times

* Midday: 12:35 PM CT
* Evening: 9:15 PM CT

# Example: Presentation

[Frequency Chart (LotteryInformation)](https://www.lotteryinformation.us/apps/freq-chart.php?state=IL&game=IAILMID3&drawset=2&ball=ALL_REG&orderby=number&tb_state=&tb_links=&tb_country=US&tb_lang=0&adsurl=&tbsite=0000&d=lotteryinformation.us)

# Source: Lottery Post

|Result|Link|
|------|------|
|Midday|https://www.lotterypost.com/game/53/results|
|Evening|https://www.lotterypost.com/game/49/results|

```html
<div class="draw horiz">
    <div class="resultsDrawDate">Saturday, November 21, 2020</div>
    <div class="drawWrap drawWrapWithTOD">
        <div class="resultsTOD"><i class="TODmid"></i><br>Midday</div>
        <div class="resultsRow"><ul class="resultsNums"><li>6</li><li>7</li><li>8</li></ul></div>
        <div class="resultsRow">Fireball: <ul class="resultsNums"><li class="orange">4</li></ul></div>
        <div class="resultsLinks">&nbsp;&nbsp;<a href="/game/53/prizes/2020/11/21" title="Pick 3 Midday prizes and odds">Prizes/Odds</a>&nbsp;•&nbsp;<a href="javascript:;" aria-label="Speak the winning numbers" class="speak speakresults" data-drawingid="5790245" data-speak="The Illinois Pick 3 Midday results for Saturday, November 21, are|6-7-8, Fireball: 4" title="Speak the winning numbers">Speak</a>
        </div>
    </div>
</div>
```

# Source: Magayo API 

Free Account rate limited to 10 calls per month

|Game|API Example|
|------|------|
|us_il_pick3_mid|https://www.magayo.com/api/results.php?api_key=AnDj7DVhGRUsk8jiYf&game=us_il_pick3_mid|
|us_il_pick3_eve|https://www.magayo.com/api/results.php?api_key=AnDj7DVhGRUsk8jiYf&game=us_il_pick3_eve|

## Optional Params

### draw

The date of the draw for which you would like to retrieve the draw results. This parameter is optional. If not specified, the latest draw results in our database will be returned.

YYYY-MM-DD
Example: 2015-08-28

### format

The API response format. This parameter is optional and the default format is JSON.

json or xml