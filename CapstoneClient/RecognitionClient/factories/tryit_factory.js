"use strict";

app.factory('TryItFactory', function(){
        let saved_info = [];

        return {
            setsavedinfo (information) {
                saved_info = information;
            },
            getsavedinfo () {
                return saved_info;
            }
        };
});