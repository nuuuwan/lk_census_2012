# Sri Lanka — Census of Population and Housing 2012

Processed data from Sri Lanka's **Census of Population and Housing 2012**,
organised into clean CSV tables with statistics at every administrative level.

## Source

Originally extracted from [@alexstorer/srilanka](https://github.com/alexstorer/srilanka),
an app built by @alexstorer for the Department of Census and Statistics and the World Bank.
The source data has since been removed, but the app remains accessible
[here](https://s3-us-west-2.amazonaws.com/worldbank-srilanka/choropleth-example.html).

## Region Hierarchy

Each CSV row is identified by a `region_id` covering one of five administrative levels:

| Level | Example | ID length | Count |
|-------|---------|-----------|-------|
| GND (Grama Niladhari Division) | `LK_1127055` | 10 chars | 14,026 |
| DSD (Divisional Secretariat Division) | `LK_1127` | 7 chars | 356 |
| District | `LK_11` | 5 chars | 25 |
| Province | `LK_1` | 4 chars | 9 |
| Country | `LK` | 2 chars | 1 |

The hierarchy runs GND → DSD → District → Province → Country.
Each table includes aggregated rows for all parent levels, computed by summing GND values.

## Data Format

**25 CSV files** in `data/`, one per census table, named:

```
<NN>-<type>-<table_name>.csv
```

- `<NN>` — zero-padded table number
- `<type>` — `person` (population statistics) or `household` (housing statistics)
- `<table_name>` — lower_snake_case table title

Each file has a `region_id` column followed by lower_snake_case field columns.

## Person (Population) Tables

### `00-person-total_population.csv`

Fields: `total_population`

*First 10 rows:*

|region_id|total_population|
|---|---:|
|LK|20,359,054|
|LK_1|5,850,745|
|LK_11|2,323,964|
|LK_1103|323,223|
|LK_1103005|7,829|
|LK_1103010|28,003|
|LK_1103015|17,757|
|LK_1103020|12,970|
|LK_1103025|8,809|
|LK_1103030|13,625|

### `01-person-ethnicity_of_population.csv`

Fields: `total_population`, `sinhalese`, `sri_lankan_tamil`, `indian_tamil`, `moor`, `burgher`, `malay`, `chetty`, `bharatha`, `other`

*First 10 rows:*

|region_id|total_population|sinhalese|sri_lankan_tamil|indian_tamil|moor|burgher|malay|chetty|bharatha|other|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|20,359,054|15,249,936|2,269,129|839,475|1,892,633|38,292|44,130|5,589|1,713|18,157|
|LK_1|5,850,745|4,925,402|339,233|56,614|460,545|25,277|27,853|4,806|1,297|9,718|
|LK_11|2,323,964|1,778,826|234,953|24,260|249,604|13,305|14,444|909|686|6,977|
|LK_1103|323,223|80,715|100,568|6,252|129,490|1,388|3,687|363|155|605|
|LK_1103005|7,829|3,217|2,793|81|1,684|28|24|0|0|2|
|LK_1103010|28,003|8,567|10,321|1,293|7,503|96|151|15|9|48|
|LK_1103015|17,757|5,431|8,522|459|3,149|67|70|10|3|46|
|LK_1103020|12,970|3,752|3,879|130|5,133|39|37|0|0|0|
|LK_1103025|8,809|4,039|2,187|92|2,302|52|91|0|0|46|
|LK_1103030|13,625|4,409|6,433|358|2,273|34|88|1|10|19|

### `02-person-religious_affiliation_of_population.csv`

Fields: `total_population`, `buddhist`, `hindu`, `islam`, `roman_catholic`, `other_christian`, `other`

*First 10 rows:*

|region_id|total_population|buddhist|hindu|islam|roman_catholic|other_christian|other|
|---|---:|---:|---:|---:|---:|---:|---:|
|LK|20,359,054|14,271,956|2,561,148|1,967,503|1,261,140|290,920|6,387|
|LK_1|5,850,745|4,293,801|278,817|501,369|651,432|121,983|3,343|
|LK_11|2,323,964|1,632,125|186,303|274,067|162,260|66,947|2,262|
|LK_1103|323,223|61,448|73,374|135,000|42,435|10,715|251|
|LK_1103005|7,829|2,689|1,644|1,862|1,039|585|10|
|LK_1103010|28,003|3,634|7,922|7,871|6,563|1,998|15|
|LK_1103015|17,757|2,340|6,659|3,279|4,128|1,347|4|
|LK_1103020|12,970|3,044|2,703|5,333|1,460|429|1|
|LK_1103025|8,809|3,305|1,478|2,470|1,191|352|13|
|LK_1103030|13,625|2,588|5,372|2,428|2,735|486|16|

### `03-person-relationship_to_household_head_of_population.csv`

Fields: `total_population`, `head`, `wife_husband`, `son_daughter`, `son_daughter_in_law`, `grandchild_great_grand_child`, `parent_of_head_or_spouse`, `other_relative`, `domestic_employee`, `boarder`, `non_relative`, `clergy`, `not_stated`

*First 10 rows:*

|region_id|total_population|head|wife_husband|son_daughter|son_daughter_in_law|grandchild_great_grand_child|parent_of_head_or_spouse|other_relative|domestic_employee|boarder|non_relative|clergy|not_stated|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|20,359,439|5,264,792|3,656,898|7,679,004|630,470|1,102,423|520,726|807,579|46,969|65,254|550,945|34,376|3|
|LK_1|5,851,130|1,482,377|1,045,034|2,065,230|195,075|320,446|175,638|296,767|30,997|34,267|195,850|9,448|1|
|LK_11|2,324,349|572,552|401,543|791,592|72,967|121,778|68,854|143,988|21,358|19,361|106,751|3,604|1|
|LK_1103|323,257|68,249|44,925|116,262|12,669|26,811|7,733|31,526|788|1,840|11,967|487|0|
|LK_1103005|7,829|1,744|1,167|3,041|288|636|204|636|1|7|101|4|0|
|LK_1103010|28,003|6,304|4,281|10,504|956|1,754|971|2,281|111|149|601|91|0|
|LK_1103015|17,757|3,969|2,815|6,536|561|1,107|561|1,497|54|76|554|27|0|
|LK_1103020|12,970|2,916|1,864|5,138|455|993|293|1,136|5|34|124|12|0|
|LK_1103025|8,809|1,995|1,296|3,310|367|725|172|723|14|14|189|4|0|
|LK_1103030|13,625|3,236|2,333|5,249|340|699|427|1,018|28|27|252|16|0|

### `04-person-gender_of_population.csv`

Fields: `total_population`, `male`, `female`

*First 10 rows:*

|region_id|total_population|male|female|
|---|---:|---:|---:|
|LK|20,359,439|9,856,633|10,502,806|
|LK_1|5,851,130|2,848,649|3,002,481|
|LK_11|2,324,349|1,140,472|1,183,877|
|LK_1103|323,257|162,798|160,459|
|LK_1103005|7,829|4,017|3,812|
|LK_1103010|28,003|14,029|13,974|
|LK_1103015|17,757|8,794|8,963|
|LK_1103020|12,970|6,505|6,465|
|LK_1103025|8,809|4,367|4,442|
|LK_1103030|13,625|6,602|7,023|

### `05-person-marital_status_of_population.csv`

Fields: `total_population`, `never_married`, `married_registered`, `married_customary`, `widowed`, `divorced`, `legally_separated`, `separated_not_legally`, `not_stated`

*First 10 rows:*

|region_id|total_population|never_married|married_registered|married_customary|widowed|divorced|legally_separated|separated_not_legally|not_stated|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|20,359,439|9,055,540|9,909,769|415,866|793,088|41,194|30,920|113,061|1|
|LK_1|5,851,130|2,563,742|2,928,377|95,277|215,202|13,253|8,077|27,202|0|
|LK_11|2,324,349|1,033,373|1,164,286|36,729|72,445|5,698|3,040|8,778|0|
|LK_1103|323,257|154,804|151,927|5,225|8,742|906|401|1,252|0|
|LK_1103005|7,829|3,768|3,732|76|195|10|12|36|0|
|LK_1103010|28,003|13,169|12,920|873|844|44|32|121|0|
|LK_1103015|17,757|8,404|8,498|294|443|31|20|67|0|
|LK_1103020|12,970|6,287|6,290|91|198|14|20|70|0|
|LK_1103025|8,809|4,139|4,333|45|204|24|17|47|0|
|LK_1103030|13,625|6,425|6,410|381|338|13|14|44|0|

### `06-person-age_group_of_population.csv`

Fields: `total_population`, `less_than_10`, `10_19`, `20_29`, `30_39`, `40_49`, `50_59`, `60_69`, `70_79`, `80_89`, `90_and_above`

*First 10 rows:*

|region_id|total_population|less_than_10|10_19|20_29|30_39|40_49|50_59|60_69|70_79|80_89|90_and_above|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|20,359,439|3,491,614|3,284,301|3,085,730|3,048,492|2,645,039|2,283,690|1,551,199|695,600|232,820|40,954|
|LK_1|5,851,130|897,992|873,726|920,382|919,624|791,588|662,567|476,368|218,065|76,894|13,924|
|LK_11|2,324,349|339,498|340,253|380,707|362,784|317,566|267,597|192,152|87,211|30,497|6,084|
|LK_1103|323,257|55,685|54,797|52,658|47,562|43,071|35,654|22,130|8,570|2,522|608|
|LK_1103005|7,829|1,604|1,373|1,262|1,251|944|796|400|131|52|16|
|LK_1103010|28,003|4,932|4,738|4,379|4,220|3,702|2,920|1,944|834|239|95|
|LK_1103015|17,757|3,045|2,791|3,101|2,688|2,321|1,872|1,271|481|159|28|
|LK_1103020|12,970|2,834|2,415|2,066|1,940|1,687|1,147|581|238|52|10|
|LK_1103025|8,809|1,529|1,495|1,406|1,357|1,198|953|555|213|75|28|
|LK_1103030|13,625|2,224|2,229|2,146|2,002|1,851|1,646|1,021|368|117|21|

## Household Tables

### `07-household-living_quarters.csv`

Fields: `total_living_quarters`, `housing_unit`, `collective_living_quarter`, `non_housing_unit`

*First 10 rows:*

|region_id|total_living_quarters|housing_unit|collective_living_quarter|non_housing_unit|
|---|---:|---:|---:|---:|
|LK|5,953,666|5,894,247|52,284|7,135|
|LK_1|1,666,854|1,642,201|20,704|3,949|
|LK_11|653,381|640,602|10,116|2,663|
|LK_1103|74,979|73,326|930|723|
|LK_1103005|1,823|1,818|4|1|
|LK_1103010|6,714|6,631|75|8|
|LK_1103015|4,285|4,231|47|7|
|LK_1103020|3,069|3,057|9|3|
|LK_1103025|2,044|2,028|8|8|
|LK_1103030|3,745|3,717|21|7|

### `08-household-occupation_status_of_housing_units.csv`

Fields: `total_housing_units`, `occupied`, `vacant`

*First 10 rows:*

|region_id|total_housing_units|occupied|vacant|
|---|---:|---:|---:|
|LK|5,894,247|5,207,740|686,507|
|LK_1|1,642,201|1,463,595|178,606|
|LK_11|640,602|562,550|78,052|
|LK_1103|73,326|65,831|7,495|
|LK_1103005|1,818|1,687|131|
|LK_1103010|6,631|6,143|488|
|LK_1103015|4,231|3,874|357|
|LK_1103020|3,057|2,821|236|
|LK_1103025|2,028|1,866|162|
|LK_1103030|3,717|3,164|553|

### `09-household-type_of_housing_unit.csv`

Fields: `total_housing_units`, `permanent`, `semi_permanent`, `improvised`, `unclassified`

*First 10 rows:*

|region_id|total_housing_units|permanent|semi_permanent|improvised|unclassified|
|---|---:|---:|---:|---:|---:|
|LK|5,207,740|4,238,491|927,408|40,464|1,377|
|LK_1|1,463,595|1,340,266|118,587|4,326|416|
|LK_11|562,550|526,635|34,452|1,227|236|
|LK_1103|65,831|60,512|5,157|121|41|
|LK_1103005|1,687|1,175|493|19|0|
|LK_1103010|6,143|5,580|562|1|0|
|LK_1103015|3,874|3,679|192|3|0|
|LK_1103020|2,821|1,794|1,013|14|0|
|LK_1103025|1,866|1,638|226|2|0|
|LK_1103030|3,164|2,902|257|5|0|

### `10-household-structure_of_housing_units.csv`

Fields: `total_housing_units`, `single_house_single_floor`, `single_house_double_floor`, `single_house_more_than_2_floors`, `attached_house_annex`, `flat`, `condominium`, `twin_house`, `row_house_line_room`, `hut_shanty`

*First 10 rows:*

|region_id|total_housing_units|single_house_single_floor|single_house_double_floor|single_house_more_than_2_floors|attached_house_annex|flat|condominium|twin_house|row_house_line_room|hut_shanty|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|4,416,584|376,764|27,654|51,424|32,127|4,179|36,512|185,131|77,365|
|LK_1|1,463,595|1,114,704|210,173|15,240|32,924|26,985|4,179|7,839|41,806|9,745|
|LK_11|562,550|353,461|124,135|12,236|20,403|24,718|4,179|3,192|15,294|4,932|
|LK_1103|65,831|26,939|14,750|3,121|2,181|8,958|941|358|6,858|1,725|
|LK_1103005|1,687|945|208|7|75|0|0|84|143|225|
|LK_1103010|6,143|3,224|1,826|210|176|208|59|69|295|76|
|LK_1103015|3,874|1,669|785|125|572|343|3|59|290|28|
|LK_1103020|2,821|810|147|12|24|16|0|5|1,366|441|
|LK_1103025|1,866|1,076|441|44|9|49|0|11|218|18|
|LK_1103030|3,164|1,412|665|167|123|457|32|8|219|81|

### `11-household-wall_type_in_housing_units.csv`

Fields: `total_housing_units`, `brick`, `cement_block_stone`, `cabook`, `soil_bricks`, `mud`, `cadjan_palmyrah`, `plank_metal_sheet`, `other`

*First 10 rows:*

|region_id|total_housing_units|brick|cement_block_stone|cabook|soil_bricks|mud|cadjan_palmyrah|plank_metal_sheet|other|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|2,764,566|1,761,898|111,130|147,320|261,260|46,117|101,935|13,514|
|LK_1|1,463,595|589,620|695,700|78,312|24,864|33,606|1,498|37,044|2,951|
|LK_11|562,550|240,504|269,310|28,313|4,002|2,926|363|16,229|903|
|LK_1103|65,831|35,430|26,173|965|78|27|114|2,939|105|
|LK_1103005|1,687|455|863|2|0|0|0|355|12|
|LK_1103010|6,143|2,534|3,369|22|2|2|2|212|0|
|LK_1103015|3,874|2,093|1,620|28|5|2|0|125|1|
|LK_1103020|2,821|1,394|583|11|3|1|13|815|1|
|LK_1103025|1,866|715|1,036|16|0|0|1|98|0|
|LK_1103030|3,164|1,798|1,191|14|3|5|0|152|1|

### `12-household-floor_type_in_housing_unit.csv`

Fields: `total_housing_units`, `cement`, `tile_granite_terrazo`, `mud`, `wood`, `sand`, `concrete`, `other`

*First 10 rows:*

|region_id|total_housing_units|cement|tile_granite_terrazo|mud|wood|sand|concrete|other|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|3,773,868|633,334|391,596|4,636|30,060|355,675|18,571|
|LK_1|1,463,595|988,077|362,744|18,793|1,368|1,808|87,362|3,443|
|LK_11|562,550|348,238|188,050|3,053|891|500|20,749|1,069|
|LK_1103|65,831|49,652|15,217|181|210|48|381|142|
|LK_1103005|1,687|1,521|97|12|8|8|41|0|
|LK_1103010|6,143|4,146|1,882|4|2|1|63|45|
|LK_1103015|3,874|2,885|964|8|4|2|7|4|
|LK_1103020|2,821|2,567|144|27|6|10|67|0|
|LK_1103025|1,866|1,556|276|3|3|0|26|2|
|LK_1103030|3,164|2,267|885|6|0|0|6|0|

### `13-household-roof_type_in_housing_unit.csv`

Fields: `total_housing_units`, `tile`, `asbestos`, `concrete`, `zink_aluminium_sheet`, `metal_sheet`, `cadjan_palmyrah_straw`, `other`

*First 10 rows:*

|region_id|total_housing_units|tile|asbestos|concrete|zink_aluminium_sheet|metal_sheet|cadjan_palmyrah_straw|other|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|2,479,226|1,800,077|213,587|49,433|544,211|109,623|11,583|
|LK_1|1,463,595|535,036|729,628|112,095|11,063|69,649|3,533|2,591|
|LK_11|562,550|89,873|363,413|78,800|4,563|24,220|476|1,205|
|LK_1103|65,831|5,210|38,809|16,788|941|3,700|126|257|
|LK_1103005|1,687|35|1,047|141|37|418|6|3|
|LK_1103010|6,143|652|3,737|1,255|39|453|4|3|
|LK_1103015|3,874|325|2,323|1,025|70|126|1|4|
|LK_1103020|2,821|44|1,720|127|351|564|13|2|
|LK_1103025|1,866|97|1,336|202|35|146|1|49|
|LK_1103030|3,164|318|1,887|735|8|208|4|4|

### `14-household-persons_living_in_housing_unit.csv`

Fields: `total_housing_units`, `1_person`, `2_persons`, `3_persons`, `4_persons`, `5_persons`, `6_persons`, `7_persons`, `8_persons`, `9_persons`, `10_or_more`

*First 10 rows:*

|region_id|total_housing_units|1_person|2_persons|3_persons|4_persons|5_persons|6_persons|7_persons|8_persons|9_persons|10_or_more|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|370,302|777,417|1,139,741|1,328,585|883,189|435,849|153,246|64,024|27,969|27,418|
|LK_1|1,463,595|99,409|211,509|310,226|379,989|249,674|127,302|44,533|19,998|9,330|11,625|
|LK_11|562,550|35,364|82,334|117,582|142,044|94,168|51,190|18,976|9,351|4,779|6,762|
|LK_1103|65,831|3,207|6,899|10,400|13,779|12,169|8,366|4,071|2,488|1,540|2,912|
|LK_1103005|1,687|88|167|253|386|319|227|105|58|43|41|
|LK_1103010|6,143|288|655|1,060|1,393|1,207|786|330|184|102|138|
|LK_1103015|3,874|156|424|704|912|731|463|204|125|74|81|
|LK_1103020|2,821|157|275|464|629|506|387|195|82|49|77|
|LK_1103025|1,866|101|193|290|413|341|231|113|76|49|59|
|LK_1103030|3,164|156|393|565|811|568|373|153|62|41|42|

### `15-household-households_living_in_housing_unit.csv`

Fields: `total_housing_units`, `1_household`, `2_households`, `3_households`, `4_households`, `5_or_more`

*First 10 rows:*

|region_id|total_housing_units|1_household|2_households|3_households|4_households|5_or_more|
|---|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|5,155,404|48,936|2,863|380|157|
|LK_1|1,463,595|1,447,197|14,744|1,288|243|123|
|LK_11|562,550|554,063|7,433|804|168|82|
|LK_1103|65,831|63,893|1,589|262|63|24|
|LK_1103005|1,687|1,636|46|5|0|0|
|LK_1103010|6,143|6,008|116|13|5|1|
|LK_1103015|3,874|3,792|73|7|2|0|
|LK_1103020|2,821|2,741|70|6|3|1|
|LK_1103025|1,866|1,761|85|17|2|1|
|LK_1103030|3,164|3,105|50|8|0|1|

### `16-household-rooms_in_housing_unit.csv`

Fields: `total_housing_units`, `1_room`, `2_rooms`, `3_rooms`, `4_rooms`, `5_rooms`, `6_rooms`, `7_rooms`, `8_rooms`, `9_rooms`, `10_and_above`

*First 10 rows:*

|region_id|total_housing_units|1_room|2_rooms|3_rooms|4_rooms|5_rooms|6_rooms|7_rooms|8_rooms|9_rooms|10_and_above|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|428,125|411,004|816,737|1,182,512|1,176,715|711,365|297,510|107,547|41,359|34,866|
|LK_1|1,463,595|137,449|100,699|204,683|356,696|346,714|182,871|76,047|31,628|13,957|12,851|
|LK_11|562,550|52,342|42,408|89,245|138,600|119,862|62,876|29,360|14,105|6,862|6,890|
|LK_1103|65,831|12,123|10,293|18,173|15,031|5,964|2,358|910|465|223|291|
|LK_1103005|1,687|259|347|605|326|113|25|5|3|3|1|
|LK_1103010|6,143|635|654|1,575|1,614|962|375|173|85|39|31|
|LK_1103015|3,874|415|544|1,113|1,035|436|187|73|30|22|19|
|LK_1103020|2,821|786|724|880|287|94|30|6|8|2|4|
|LK_1103025|1,866|299|319|646|348|137|66|23|13|4|11|
|LK_1103030|3,164|261|354|819|1,064|450|142|41|17|11|5|

### `17-household-year_of_construction_of_housing_unit.csv`

Fields: `total_housing_units`, `2011`, `2010`, `2009`, `2008`, `2007`, `2006`, `2005`, `2000_2004`, `1995_1999`, `1990_1994`, `1980_1989`, `before_80`

*First 10 rows:*

|region_id|total_housing_units|2011|2010|2009|2008|2007|2006|2005|2000_2004|1995_1999|1990_1994|1980_1989|before_80|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,207,740|323,194|236,190|210,782|205,037|206,425|210,202|256,804|819,104|581,580|477,621|620,287|1,060,514|
|LK_1|1,463,595|78,082|52,741|51,450|53,631|55,679|56,698|73,748|237,869|167,458|142,173|184,008|310,058|
|LK_11|562,550|25,978|18,707|18,721|19,853|20,924|22,058|29,153|88,776|62,129|55,381|74,862|126,008|
|LK_1103|65,831|1,764|1,327|1,460|1,597|2,036|2,201|3,065|8,113|6,518|6,596|9,511|21,643|
|LK_1103005|1,687|42|51|60|51|65|113|187|371|239|198|192|118|
|LK_1103010|6,143|234|144|178|181|233|265|590|979|766|822|958|793|
|LK_1103015|3,874|115|92|100|81|103|127|164|493|563|670|432|934|
|LK_1103020|2,821|123|95|116|121|330|175|160|390|305|343|379|284|
|LK_1103025|1,866|83|55|64|54|95|87|121|252|184|138|195|538|
|LK_1103030|3,164|72|68|68|88|74|98|136|460|297|533|368|902|

### `18-household-source_of_drinking_water_of_household.csv`

Fields: `total_households`, `protected_well_within_premises`, `protected_well_outside_premises`, `unprotected_well`, `tap_within_unit_main_line`, `tap_within_premises_but_outside_unit_main_line`, `tap_outside_premises_main_line`, `rural_water_projects`, `tube_well`, `bowser`, `river_tank_stream`, `rain_water`, `bottled_water`, `other`

*First 10 rows:*

|region_id|total_households|protected_well_within_premises|protected_well_outside_premises|unprotected_well|tap_within_unit_main_line|tap_within_premises_but_outside_unit_main_line|tap_outside_premises_main_line|rural_water_projects|tube_well|bowser|river_tank_stream|rain_water|bottled_water|other|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|LK|5,264,282|1,652,972|772,819|211,556|1,110,050|363,043|181,235|482,937|177,432|18,931|239,952|4,022|9,984|39,349|
|LK_1|1,482,221|579,651|96,365|28,587|550,564|65,757|49,380|51,494|44,864|609|6,767|333|1,476|6,374|
|LK_11|572,475|123,735|11,188|1,951|360,380|29,938|26,539|12,728|2,065|38|1,560|112|828|1,413|
|LK_1103|68,245|377|67|28|52,514|4,885|9,711|0|444|2|2|14|40|161|
|LK_1103005|1,743|7|1|0|1,422|79|224|0|2|0|0|0|0|8|
|LK_1103010|6,304|81|7|9|5,048|441|610|0|82|0|1|0|8|17|
|LK_1103015|3,967|33|2|1|3,209|521|150|0|16|0|0|0|0|35|
|LK_1103020|2,916|10|2|0|2,283|121|486|0|1|1|0|0|1|11|
|LK_1103025|1,995|9|0|0|1,364|165|436|0|8|0|0|0|0|13|
|LK_1103030|3,236|16|2|2|2,666|160|382|0|8|0|0|0|0|0|

### `19-household-cooking_fuel_of_household.csv`

Fields: `total_households`, `fire_wood`, `kerosene`, `gas`, `electricity`, `saw_dust_paddy_husk`, `other`

*First 10 rows:*

|region_id|total_households|fire_wood|kerosene|gas|electricity|saw_dust_paddy_husk|other|
|---|---:|---:|---:|---:|---:|---:|---:|
|LK|5,264,282|4,124,667|129,896|975,262|9,770|7,606|17,081|
|LK_1|1,482,221|778,323|89,929|598,250|3,405|1,152|11,162|
|LK_11|572,475|165,027|54,411|346,340|1,957|432|4,308|
|LK_1103|68,245|2,982|22,858|41,776|231|7|391|
|LK_1103005|1,743|212|1,041|481|1|0|8|
|LK_1103010|6,304|447|1,864|3,936|16|2|39|
|LK_1103015|3,967|210|1,117|2,627|6|1|6|
|LK_1103020|2,916|244|1,894|766|2|0|10|
|LK_1103025|1,995|222|718|1,023|6|0|26|
|LK_1103030|3,236|146|739|2,327|20|0|4|

### `20-household-lighting_of_household.csv`

Fields: `total_households`, `electricity_national_electricity_network`, `electricity_rural_hydro_electricity_projects`, `kerosene`, `solar_power`, `bio_gas`, `other`

*First 10 rows:*

|region_id|total_households|electricity_national_electricity_network|electricity_rural_hydro_electricity_projects|kerosene|solar_power|bio_gas|other|
|---|---:|---:|---:|---:|---:|---:|---:|
|LK|5,264,282|4,577,662|8,549|640,265|33,597|133|4,076|
|LK_1|1,482,221|1,426,414|0|53,546|773|31|1,457|
|LK_11|572,475|559,218|0|12,586|158|13|500|
|LK_1103|68,245|65,133|0|2,990|19|6|97|
|LK_1103005|1,743|1,449|0|292|0|0|2|
|LK_1103010|6,304|6,060|0|208|0|6|30|
|LK_1103015|3,967|3,861|0|99|1|0|6|
|LK_1103020|2,916|2,299|0|613|2|0|2|
|LK_1103025|1,995|1,886|0|100|0|0|9|
|LK_1103030|3,236|3,102|0|133|1|0|0|

### `21-household-toilet_facilities_of_household.csv`

Fields: `total_households`, `water_seal_and_connected_to_a_piped_sewer_system`, `water_seal_and_connected_to_a_septic_tank`, `pour_flush_toilet_not_water_seal`, `direct_pit`, `other`, `not_using_a_toilet`

*First 10 rows:*

|region_id|total_households|water_seal_and_connected_to_a_piped_sewer_system|water_seal_and_connected_to_a_septic_tank|pour_flush_toilet_not_water_seal|direct_pit|other|not_using_a_toilet|
|---|---:|---:|---:|---:|---:|---:|---:|
|LK|5,264,282|4,683,248|240,322|111,732|136,544|4,154|88,282|
|LK_1|1,482,221|1,311,882|126,649|21,733|17,892|2,193|1,872|
|LK_11|572,475|457,919|95,894|8,172|8,631|1,534|325|
|LK_1103|68,245|22,210|44,053|781|664|477|60|
|LK_1103005|1,743|1,408|258|49|10|16|2|
|LK_1103010|6,304|3,721|2,404|78|90|8|3|
|LK_1103015|3,967|942|2,975|4|19|4|23|
|LK_1103020|2,916|2,055|739|3|98|16|5|
|LK_1103025|1,995|639|1,286|37|4|26|3|
|LK_1103030|3,236|563|2,651|0|22|0|0|

### `22-household-communication_items_owned_by_household.csv`

Fields: `radio`, `tv`, `fixed_tp`, `mobile`, `pc`, `laptop`, `fax`

*First 10 rows:*

|region_id|radio|tv|fixed_tp|mobile|pc|laptop|fax|
|---|---:|---:|---:|---:|---:|---:|---:|
|LK||||||||
|LK_1|1,803.0388|2,128.5738|1,162.6966|2,074.7197|528.9158|203.2947|14.4499|
|LK_11|409.9789|491.5007|278.0746|478.0951|149.8836|77.8987|6.0709|
|LK_1100|0.6261|0.8311|0.351|0.8094|0.1303|0.0241|0.0024|
|LK_1100000|0.6261|0.8311|0.351|0.8094|0.1303|0.0241|0.0024|
|LK_1103|22.8472|29.4096|14.0366|28.4157|6.9658|3.9754|0.3228|
|LK_1103005|0.6104|0.7384|0.1526|0.7476|0.062|0.0115|0.0006|
|LK_1103010|0.6745|0.8555|0.3966|0.8474|0.2341|0.1194|0.0071|
|LK_1103015|0.6854|0.884|0.3995|0.8447|0.2044|0.1051|0.0066|
|LK_1103020|0.4853|0.6231|0.1296|0.6492|0.0432|0.0103|0.0007|

### `23-household-solid_waste_disposal_by_household.csv`

Fields: `total_households`, `collected_by_local_authorities`, `occupants_burn`, `occupants_bury`, `occupants_composting_solid_waste`, `occupants_dispose_solid_waste_into_road_river_canal_sea_creek_forest_etc`, `other`

*First 10 rows:*

|region_id|total_households|collected_by_local_authorities|occupants_burn|occupants_bury|occupants_composting_solid_waste|occupants_dispose_solid_waste_into_road_river_canal_sea_creek_forest_etc|other|
|---|---:|---:|---:|---:|---:|---:|---:|
|LK|5,264,282|1,077,950|2,486,628|1,228,751|406,606|46,526|17,821|
|LK_1|1,482,221|618,269|593,413|202,000|58,266|5,683|4,590|
|LK_11|572,475|394,117|112,584|42,997|18,374|2,218|2,185|
|LK_1103|68,245|66,936|268|120|14|595|312|
|LK_1103005|1,743|1,740|2|1|0|0|0|
|LK_1103010|6,304|6,186|18|11|1|5|83|
|LK_1103015|3,967|3,943|7|8|1|6|2|
|LK_1103020|2,916|2,894|0|0|0|22|0|
|LK_1103025|1,995|1,983|9|1|0|0|2|
|LK_1103030|3,236|3,186|20|5|1|24|0|

### `24-household-housing_ownership_status_of_household.csv`

Fields: `total_households`, `owned_by_a_household_member`, `rent_lease_government_owned`, `rent_lease_privately_owned`, `occupied_free_of_rent`, `encroached`, `other`

*First 10 rows:*

|region_id|total_households|owned_by_a_household_member|rent_lease_government_owned|rent_lease_privately_owned|occupied_free_of_rent|encroached|other|
|---|---:|---:|---:|---:|---:|---:|---:|
|LK|5,264,282|4,365,190|116,871|330,410|328,346|68,650|54,815|
|LK_1|1,482,221|1,169,052|41,780|186,677|50,683|17,770|16,259|
|LK_11|572,475|427,264|24,830|90,417|17,221|7,478|5,265|
|LK_1103|68,245|47,723|6,104|11,434|1,777|813|394|
|LK_1103005|1,743|1,272|31|194|22|216|8|
|LK_1103010|6,304|4,432|278|1,285|187|67|55|
|LK_1103015|3,967|2,622|119|1,056|108|29|33|
|LK_1103020|2,916|2,063|228|375|244|2|4|
|LK_1103025|1,995|1,581|88|215|95|4|12|
|LK_1103030|3,236|1,956|374|828|63|3|12|

## Regenerating the Data

```bash
python src/lk_census_2012/build_csvs.py
python src/lk_census_2012/build_readme.py
```
