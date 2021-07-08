
# CLOUDANT SYNTAX

<https://cloud.ibm.com/apidocs/cloudant#postfind>

## Find

Query via selector.

```json
{
   "selector": {
      "timestamp": {
         "$gte": 1605852000
      }
   },
   "fields": [
      "_id",
      "_rev",
      "ball",
      "date",
      "timestamp"
   ],
   "skip": 0
}
```

## Views

### Create View

<https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-views-mapreduce>

[Map](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-views-mapreduce#map-function-examples)

```json
example
```

[Reduce](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-views-mapreduce#reduce-functions)


```json
{
    "views" : {
        "countFireball" : {
            "map" : "function(doc) {  emit(doc.ball, 1); }",
        "reduce": "_sum"
        }
    }
}
```

### Query A View

<https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-using-views>

`lottodb/_design/countFireballDesign/_view/by_ball?group=true`

```json

{"rows":[
    {"key":"0","value":66},
    {"key":"1","value":73},
    {"key":"2","value":80},
    {"key":"3","value":52},
    {"key":"4","value":68},
    {"key":"5","value":63},
    {"key":"6","value":59},
    {"key":"7","value":70},
    {"key":"8","value":64},
    {"key":"9","value":58}
]}

```
