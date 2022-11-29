# About
This script will download:
* all your bookmarked tweets
* any replied-to or quoted tweets, any tweets replied-to or quoted by those tweets, etc. 
* images and videos attached to tweets

It will also expand t.co links to their full URLs. If you bookmarked one tweet in a thread, this script will grab all tweets _above_ the bookmarked one in the thread, but not tweets _below_ the bookmarked one.

Without academic/enterprise access to the Twitter API, it's somwehat difficult to get posts from a thread after the referenced tweet, so uhh I guess just bookmark the last tweet of every thread you want downloaded.

## Technical
The tweets are saved to a JSON file in this form:
```
{
    "attachments": {
      "polls": [ 
        {
          "end_time": "2021-09-08T20:25:45.000Z",
          "id": "1",
          "options": [
            {
              "label": "love it",
              "position": 1,
              "votes": 1
            }
          ],
          "voting_status": "closed"
        }
      ],
      "media": [
        {
          "key": "3_123",
          "type": "photo",
          "url": "https://pbs.twimg.com/media/abcdef.jpg"
        }
      ]
    },
    "author_id": "1234567890",
    "conversation_id": "9876543210",
    "id": "1111111111111",
    "in_reply_to_user_id": null,
    "referenced_tweets": [
      {
        "id": "2222222222",
        "type": "quoted"
      }
    ],
    "text": "i am a birb"
  }
```
Note that the attachment objects are _not_ in the form that the Twitter API returns them, but these objects should include all the data necessary to reproduce most of the data people care about.

# Use
## Prep
### Installing Python & pip
If you don't have Python installed (you can test this by trying to run `python -V` in your terminal), you can follow [these instructions](https://www.digitalocean.com/community/tutorials/install-python-windows-10) to install Python and pip.

### Downloading
Download and unzip the zip file for this repository by clicking the `<> Code` button.

### Installing Requirements
In your terminal, use `cd` to navigate to the `download_bookmarks_data` directory, and run:
```pip install -r requirements.txt```

### Setting Secrets
You will need my client ID and secret. Run the following in your terminal, replacing `$client_id` and `$client_secret` with the values you got from me.
```
export GET_BOOKMARKS_CLIENT_ID=$client_id GET_BOOKMARKS_CLIENT_SECRET=$client_secret
```

## Running
In your terminal, use `cd` to navigate to the `twitter_bookmarks` directory, and run the following:
```python -m download_bookmarks_data```

Once the script has completed, you should see a new directory called `twitter_bookmarks_data`. It will look like this:
```
twitter_bookmarks_data
├── bookmarks.json         // bookmarked tweets
├── referenced_tweets.json // tweets referenced by bookmarks
├── media                  // all files (images and videos) attached to tweets
│   ├── 3_123.jpg
│   ├── ... 
│   └── 3_124.mp4
└── get_bookmarks.log    // log file -- if everything goes smoothly, this can be deleted
```

You can move this directory to wherever you want it to live.

# TODO
I want to eventually set this up to render nicely with Twitter download data, but I don't have the spoons to do that right now.