db.createUser({
  user: 'airflow',
  pwd: 'airflow',
  roles: [
    {
      role: 'dbOwner',
      db: 'the_database',
    },
  ],
});

db.createCollection('jokes');

db.jokes.insert({
  error: false,
  category: 'Misc',
  type: 'single',
  joke: 'In Soviet Russia, gay sex gets you arrested. In America, getting arrested gets you gay sex.',
  flags: {
    nsfw: true,
    religious: false,
    political: false,
    racist: false,
    sexist: false,
    explicit: true
  },
  safe: false,
  id: 289,
  lang: 'en'
});