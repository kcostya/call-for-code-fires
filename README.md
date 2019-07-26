# Call for Code 2019: Fire Forecasting

### Problem Description

In the US, over the past decade, there have been an average of 66 thousand fires annually, with Federal fire suppression costs totaling over \$18 billion for the decade <cite>[(NIFC, 2019)][1]</cite>. Over 69 million acres have been burned, sometimes resulting in property damage, injury, and even death. According to the National Fire Protection Association’s Fire Loss report for the US in 2017 alone, property damage was estimated at \$23 billion, including \$10 billion in losses from wildfires in Northern California <cite>[(NFPA, 2018)][2]</cite>. 
{% include image.html url="https://raw.githubusercontent.com/kcostya/call-for-code-fires/master/images/all_fires.JPG?token=AHPSIDCTLWZAAUE3PDXU2LS5HK3CS" description="Fires 2010-2018" %}

### Forecasting Fires - Why is it important?

Fire forecasts and danger ratings “...provide quantification of risk elements that are critical for daily decisions regarding firefighter resource placement, staffing levels, appropriate suppression response, and strategic decisions at local, regional, and national levels.” <cite>[(NWCG, 2019)][3]</cite>. With advance notice, agencies will be able to prepare and mobilize more quickly; fighting fires in their early stages might lead to a reduction in fire spread and therefore, damage. Most importantly, this could prevent injury and death. In 2017 there were over 14 thousand injuries and over 3 thousand deaths due to fire <cite>[(USFA, n.d.)][4]</cite>. 

### Previous Work

One of the current fire forecasting products in use in the US is the 7-Day Significant Fire Potential Product. Per the Geographic Area Coordination Centers <cite>[(GACC, n.d.)][5]</cite>:

> The product is based on a statistical model which uses fuel moisture inputs from the NFDRS (WIMS) and various gridded weather inputs from weather models. This data is processed through a series of equations that yield forecasts of Fuel Dryness Level (DL) as well as probabilities (some objective and some subjective) of certain critical weather conditions for each of the next 7 days. When appropriate combinations of DL and weather triggers are expected, a “**High Risk Day**” is designated on the Chart to warn of a significantly higher than normal chance for a “Large Fire”.

### Solution

We seek to improve upon these models by removing some of the subjectivity and direct human involvement through the use of deep learning algorithms and remotely sensed data. Our goal is to develop a model to forecast the number of fires in an area, given ambient weather conditions, as well as some constant features like elevation, population density, etc. 

### Data

For our training, validation and test data, we considered an area which includes the states of California and Nevada, as there have been numerous large wildfires in CA in recent years which have caused injury and significant property damage. However, our data comes from near-real-time global NASA datasets, and our solution could be applied globally with only the model needing to be trained on the regional data. 

Our dataset consists of different NASA data collections, including active fire, weather, elevation, landcover, population, and vegetation data.  Our data spans 9 years (2010-2019). The temporal and spatial resolution varies between datasets, but we have aggregated and resampled the time series data to be on 12hour frequency and each cell in our spatial grid is roughly 50km<sup>2</sup>.   

##### Data Sources

1. [Fire Information Resource Management System (FIRMS)](https://doi.org/10.7927/H49C6VHW).  _Fire Information For Resource Management System (FIRMS) distributes Near Real-Time (NRT) active fire data within 3 hours of satellite observation from both the Moderate Resolution Imaging Spectroradiometer (MODIS) and the Visible Infrared Imaging Radiometer Suite (VIIRS)._ We used MODIS because VIIRS data only spans from 2012 to present.
2. [Modern-Era Retrospective analysis for Research and Applications, Version 2 (MERRA 2)](https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/) _(MERRA-2) provides data beginning in 1980 and enables assimilation of modern hyperspectral radiance and microwave observations, along with GPS-Radio Occultation datasets. It also uses NASA's ozone profile observations that began in late 2004. Spatial resolution is about 50 km in the latitudinal direction._
3. [Land Cover CCI Climate Research Data Package](http://maps.elie.ucl.ac.be/CCI/viewer/download.php) _Global [land cover] maps at 300m spatial resolution._ Updated annually.
4. [Gridded Population of the World V.4](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11). _Population Density. Estimates of human population density (# of persons/square km) based on counts consistent with national consensuses and population registers_. 30 arc-second resolution (~1km)
5. [MODIS Vegetation Indices](https://modis.gsfc.nasa.gov/data/dataprod/mod13.php) _MODIS vegetation indices, produced on 16-day intervals at 1km spatial resolution, provide consistent spatial and temporal comparisons of vegetation canopy greenness, a composite property of leaf area, chlorophyll and canopy structure._ In some cases, [vegetation indices have be used to estimate fuel moisture content](https://www.sciencedirect.com/science/article/abs/pii/S0034425704001531), one of the most important factors in fire ignition and spread.

### Architecture

[ details of final architecture here ]

### Metric

For our metric, we used [F1 Score](https://en.wikipedia.org/wiki/F1_score), [precision and recall](https://en.wikipedia.org/wiki/Precision_and_recall). For our baselines, we used scores from the following naive predictions:

1. No fires [Fscore: 0.493, Precision: 0.485, Recall: 0.500]

2. The average of the previous 2 days fire count [Fscore: 0.632, Precision: 0.611, Recall: 0.686]

3. The average of the previous 24 hours fire count [Fscore: 0.737, Precision: 0.729, Recall: 0.770]

4. The average of the previous 12 hours fire count [Fscore: 0.755, Precision: 0.767, Recall: 0.764]

   

### Results

[ details of results here ]



![loss gif](images/loss.gif)

![predicted and actual gif](images/pred_actual.gif)



### Future Work

Due to the size of our dataset, and the limitations of the machines we were training on, we were unable to use a higher temporal and spatial resolution. We believe that with higher resolution, our model's predictive power would be greatly enhanced. Preliminary runs at a 3hr resolution show [ discuss specific scores here ] , which is a [ specific score ] improvement over the 12hr resolution. 

Access to larger machines would also allow us to produce a longer-range forecast. With our current architecture, our features include not only those from the current time-step, but also those from the previous _N_ time-steps, where _N_ is equal to the number of time-steps we wish to forecast. This is very expensive, and we were limited to forecasting only 2 days. Even with a 2 day forecast, we were able to achieve [ discuss specific scores here ] , which is a [ specific  ]% improvement over the baseline 2 day forecast of [Fscore: 0.632, Precision: 0.611, Recall: 0.686]. With an extended forecast, fire agencies could better prepare themselves and advise the community in times of increased fire danger. 

We'd like to consult domain experts to further explore features which might improve our scores, such as using forecasted weather. Currently we're using historical weather data, and weather at the time of prediction to make our forecast. However, as weather is one of the major factors in fire ignition and spread, we believe that using forecasted weather for each time-step in our prediction would result in more accurate predictions, particularly when combined with a higher temporal and spatial resolution.

### Credits and Thanks

First, we'd like to thank IBM for access to [ list IBM products/services used here ] and for the opportunity to compete in this challenge. It has been an inspiring and exciting experience for us. We would love to see our work applied to help mitigate damage and injury. 

We'd also like to thank NASA and those involved in funding the collection of, and curating the datasets we have used. This would not be possible without you, so thank you! 

### License



[1]: https://www.nifc.gov/fireInfo/fireInfo_documents/SuppCosts.pdf
[2]:https://www.nfpa.org/News-and-Research/Data-research-and-tools/US-Fire-Problem/Fire-loss-in-the-United-States
[3]: https://www.nwcg.gov/sites/default/files/publications/pms426-3.pdf
[4]: https://www.usfa.fema.gov/data/statistics/
[5]: https://gacc.nifc.gov/oncc/predictive/weather/Fire%20Potential%20Documentation.htm
[6]: https://en.wikipedia.org/wiki/F1_score
[7]: https://en.wikipedia.org/wiki/Precision_and_recall



