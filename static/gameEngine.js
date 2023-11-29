const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('./mtgopen.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the mtg open database.');
  });

db.serialize(() => {
    db.run(`SELECT * FROM cards`)
})

  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Close the database connection.');
  });