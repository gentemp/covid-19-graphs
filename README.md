## Recreating online COVID-19 charts with Johns Hopkins CSSE data and matplotlib

There are many graphs and charts produced for online news articles that are
"frozen" in time. This repo attempts to re-create those graphs and charts but
with updated versions as more data become available.

I've chosen to use the [Johns Hopkins CSSE COVID-19 repo](https://github.com/CSSEGISandData/COVID-19)
as source for all data. Mostly because it's convenient but also because a lot
of people seem to use it already.

### Articles

You can find the recreated graphs, charts, figures and other content on the
[wiki](https://github.com/gentemp/covid-19-graphs/wiki).

### Notes on setup

In order to get this code to work you'll have to clone this repository and then
clone the Johns Hopkins CSSE repo and the wiki in the root folder.

```
> git clone https://github.com/gentemp/covid-19-graphs.git
> cd covid-19-graphs
> git clone https://github.com/CSSEGISandData/COVID-19.git
> git clone https://github.com/gentemp/covid-19-graphs.wiki.git
```

If all you want is to modify the scripts and run them locally you should be
fine without the wiki.