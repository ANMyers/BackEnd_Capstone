"use strict";

app.factory('TryItFactory', function(){
        let saved_info = [];

        return {
            setsavedinfo (information) {
                saved_info = information;
            },
            getsavedinfo () {
                return saved_info;
            },
            setresultsinfo (information) {
                saved_info = information;
            },
            getresultsinfo () {
                return saved_info;
            }
        };
});