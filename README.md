# beets-releasetype
A plugin for Beets to write releasetype tag to your music files. Primary releasetypes are: Single, EP or Album. There is support to set a secondary releasetype. Supported secondary releasetypes are: Compilation, Demo, DJ-mix, Live, Remix and Soundtrack.

The criteria I applied to determine the releasetype are based on [TuneCore](https://support.tunecore.com/hc/en-ca/articles/115006689928-What-is-the-difference-between-a-Single-an-EP-and-an-Album-) guidelines.

### Single
Your release will be classified as a single if:
* The release is 1-3 tracks
* The entire release is 30 minutes or less, and each individual track is less than 10 minutes long.

### EP
In order for a release to be considered an EP, it must meet one of the following two requirements:

The release has a total of 1-3 tracks, one or more of the tracks is 10 minutes or longer, and the entire release is less than 30 minutes
The release has a total of 4-6 tracks and the entire release is less than 30 minutes

### Album
Any release with seven or more tracks will be considered an album.
Any release that has 1-6 tracks but is over 30 minutes long will be considered an album.

# Getting Started
Install the plugin and make sure you using at least version 1.6.0 of beets and Python 3.8.

To use the releasetype plugin, first enable it in your configuration [see Using Plugins](https://beets.readthedocs.io/en/latest/plugins/index.html#using-plugins). 
```
plugins:
- ...
- releasetype
```
Then, install the inquirer library by typing:
`pip install inquirer`

# CLI Reference
You can write a releasetype to a single album by typing:

`beet releasetype --album 'Album name'`

`beet releasetype --a 'Album name'`

Or write the releasetype for your entire library by typing:

`beet releastype`
