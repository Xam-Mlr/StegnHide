const {app, BrowserWindow, Menu, ipcMain } = require("electron")
const {PythonShell} = require("python-shell");

root_path = app.getAppPath()



ipcMain.on('python_hide', function(event, data){

  

    let options = {  
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: [data[0], "0", data[1]]
      };

    PythonShell.run(`${root_path}/backend/env/steghide.py`, options, function (err, results) {

        console.log('results: %j', results);
        //console.log('results: %j', results[0]);

        try{
            if (results[1] == "finished"){
                event.reply("python_hide reply", "successful")
                console.warn("successful")
            }else if(results[1] == "The text couldn't be hidden into the image because the image is too small to contain this text"){
                event.reply("python_hide reply", "The text couldn't be hidden into the image because the image is too small to contain this text\nPlease extend the image or reduce the text")
                console.warn("size failure")
            }else{
                event.reply("python_hide reply","failure")
                console.warn("failure")
            }
        }catch{
            event.reply(`python_hide reply`,`full failure ${err}`)
            console.warn(`full failure ${err}`)
        }
    });
})

ipcMain.on('python_get', function(event, data){

    console.warn("ok")
    let options = {  
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: [data[0], "1", data[1]]
      };

    PythonShell.run(`${root_path}/backend/env/steghide.py`, options, function (err, results) {

        console.log('results: %j', results);

        try{
            if (results[0] != ""){
                event.reply("python_get reply", ["successful", results])
                console.warn("successful")
            } else{
                event.reply("python_get reply",["failure"])
                console.warn("failure")
            }
        }catch{
            event.reply("python_get reply",["full failure"])
            console.warn("full failure")
            console.warn(`full failure ${err}`)
        }
    });
})



function createWindow(){
    const mainWindow = new BrowserWindow({
        width:710,
        height: 850,
        minWidth: 650,
        maxWidth: 1000,
        titleBarStyle: 'hidden',
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
            contextIsolation: false,
            nodeIntegrationInWorker: true,
            nodeIntegrationInSubFrames: true
          }
    })

    mainWindow.loadFile("/Users/Maxence/Documents/MacBookPro/projects/electron/index.html")
}

app.whenReady().then(() =>{
    createWindow()
})

