# redline2timesketch
Parses the Redline CSV output in a csv that is importable by timesketch
This is a POC, it is not made to be used in a productive envirenment.

Bugs are expected.

The end goal is to migrate that to timesketch core as a import module similar to csv and json.

# redline headers
```csv
Alert,Tag,Timestamp,Field,Summary
```

# timesketch headers

```csv
message,timestamp,datetime,timestamp_desc,extra_field_1,extra_field_2
```

# Mapping

```
Alert --> Alert (extra field)
Tag --> Tag (extra field)
Timestamp --> timestamp
Timestamp --> datetime
Field --> timestamp_desc

```

# Ussage

Investigate your Host using redline, tag entries or set your filter to trim your results.
Once you are finished, export your results as a csv (make sure to do it from the timeline view, not the tags and comments view)

The result will be an results.csv

Now run redline2timesketch:
```
python2 redline2timesketch.py results.csv output.csv
```

The output.csv is ready to be imported to timesketch.

Import it via:

```
tsctl csv2ts -n test -f output.csv
```