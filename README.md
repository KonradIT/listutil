# Twitter List Clone/Fork/Mixer Utility

Script to 'clone' or 'fork' an exisiting list from another user to your profile.

Also can be run as a cron job to update members from the parent list to your list.

And can also 'remix' two or more lists together.

### Installing:

    pip install -r requirements.txt

Or if you use Pip file:

	pipenv sync
    
### Running:

Requires the following keys to be exported:

- `'TWITTER_CONSUMER_KEY'`
- `'TWITTER_CONSUMER_SECRET'`
- `'TWITTER_ACCESS_TOKEN'`
- `'TWITTER_ACCESS_TOKEN_SECRET'`

	# Fork list id to a new one by the same name and members and config
	python3 listutil.py --fork [list_id]
	
	# Update your list with members from original list, you can put this into your cron job safely (if --debug=false then clean exit = ok, stuff in stdout = errors!)
	python3 listutil.py --update --source_id [list_id] --destination_id [list_id (note it must be yours)]
	
	# Remix some lists into a new one
	python3 listutil.py --remix --name Remixed --mode public --input list1 list2 list3

### To-do / idea list:

- [ ] Accept 'slug' list string as acceptable input
- [ ] Allow custom name and privacy mode in `--fork` 
- [ ] Refactor arg parse so it uses `add_subparsers()`
- [ ] config.yaml file instead of ENV variable (or both)
