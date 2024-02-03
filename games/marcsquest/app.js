const path = require('path');
const express = require('express');
var fp = require("find-free-port")
const open = require('open');
const fs = require("fs");
const { app, BrowserWindow } = require('electron');
const { json } = require('express');

const { Database } = require('secure-db');

const db = new Database('marcsquest-data', true);
//stop the stupid default database
fs.rmSync(__dirname + "/database/your-database", { recursive: true, force: true });

db.set('init', "true");
// create express app
const expressapp = express();


/*-------------------*/

expressapp.use(express.static('.'));

expressapp.get('/', (req, res) => {
    // if (db.get("passedIntro") === "true") {
    //return res.redirect("tutorial")
    // }
    res.sendFile(__dirname + '/index.html')
})

/*-------------------*/
// find available port (if not 3000)
fp(3000).then(([freep]) => {
    const port = freep;
    const host = `http://127.0.0.1:${ port }`;
    expressapp.listen(port, async() => {
        console.log(`MarcsQuest Loading...`);
        const createWindow = () => {
            const win = new BrowserWindow({
                width: 1500,
                height: 700,
                resizable: false,

            })
            var splash = new BrowserWindow({
                width: 1000,
                height: 300,
                transparent: false,
                frame: false,
                alwaysOnTop: true,
                resizable: false,
                movable: false

            });
            splash.loadFile('./loading.html');
            splash.center();
            win.hide();
            setTimeout(function() {
                splash.hide();
                splash.close();

                win.show();
                win.setAlwaysOnTop(true);
                win.setMenuBarVisibility(false)
                win.loadURL(host)

                win.setAlwaysOnTop(false);
            }, 22000);

        }
        app.whenReady().then(() => {
            createWindow()
        })

        //open(`${ host }/`); // opens `web/index.html` page
    });

}).catch((err) => {
    console.error(err);
});