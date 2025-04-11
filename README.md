# SC4023-Project

## Sample Expected Result
```
$ python main.py ResalePricesSingapore.csv A1234567B
Loading data

---------BASIC STORE---------
              Column          Blocks
               month             381
                town             817
           flat_type             871
               block             273
         street_name            1093
        storey_range             654
      floor_area_sqm             218
          flat_model            1199
 lease_commence_date             109
        resale_price             218
               Total            5833

---------COMPRESSED STORE---------
              Column          Blocks
               month             109
                town              55
           flat_type              55
               block             164
         street_name            1093
        storey_range              55
      floor_area_sqm             218
          flat_model              55
 lease_commence_date             109
        resale_price             218
               Total            2131


Running queries for JURONG WEST from months 6 to 7 in 2017

---------FILTER PERMUTATIONS (ZM OFF; IDX OFF)---------
         Permutation               Blocks
('month', 'town', 'area')          109|111|113
('month', 'area', 'town')          109|114|116
('town', 'month', 'area')           55|151|153
('town', 'area', 'month')           55|175|270
('area', 'month', 'town')          218|327|329
('area', 'town', 'month')          218|273|368

---------FILTER PERMUTATIONS (ZM ON; IDX OFF)---------
         Permutation               Blocks
('month', 'town', 'area')          109|111|113
('month', 'area', 'town')          109|114|116
('town', 'month', 'area')           50|146|148
('town', 'area', 'month')           50|170|265
('area', 'month', 'town')          218|327|329
('area', 'town', 'month')          218|268|363

---------FILTER PERMUTATIONS (ZM OFF; IDX ON)---------
         Permutation               Blocks
('month', 'town', 'area')                3|5|7
('month', 'area', 'town')               3|8|10
('town', 'month', 'area')             55|58|60
('town', 'area', 'month')           55|175|178
('area', 'month', 'town')          218|221|223
('area', 'town', 'month')          218|273|276

---------FILTER PERMUTATIONS (ZM ON; IDX ON)---------
         Permutation               Blocks
('month', 'town', 'area')                3|5|7
('month', 'area', 'town')               3|8|10
('town', 'month', 'area')             50|53|55
('town', 'area', 'month')           50|170|173
('area', 'month', 'town')          218|221|223
('area', 'town', 'month')          218|268|271

---------INDIVIDUAL SCANS---------
9 block reads for min price
9 block reads for avg price
9 block reads for stddev price
11 block reads for min price/sqm
38 total block reads
Year,Month,town,Category,Value
2017,06,JURONG WEST,Minimum Price,300000.0
2017,06,JURONG WEST,Average Price,421762.69
2017,06,JURONG WEST,Standard Deviation of Price,78630.88
2017,06,JURONG WEST,Minimum Price per Square Meter,2869.16

---------SHARED SCANS---------
11 block reads
Year,Month,town,Category,Value
2017,06,JURONG WEST,Minimum Price,300000.0
2017,06,JURONG WEST,Average Price,421762.69
2017,06,JURONG WEST,Standard Deviation of Price,78630.88
2017,06,JURONG WEST,Minimum Price per Square Meter,2869.16

---------VECTOR AT A TIME---------
9 block reads
Year,Month,town,Category,Value
2017,06,JURONG WEST,Minimum Price,300000.0
2017,06,JURONG WEST,Average Price,421762.69
2017,06,JURONG WEST,Standard Deviation of Price,78630.88
2017,06,JURONG WEST,Minimum Price per Square Meter,2869.16
```