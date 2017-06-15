"use strict";

app.factory('TryItFactory', function(){
        let data_info = [];

        return {
            setinfo (information) {
                data_info = {
                    'algorithm': information.algorithm,
                    'sample_set': information.sample_set,
                    'variables': information.indexs,
                    'amount': information.amount
                };
            },
            getinfo () {
                return data_info;
            }
        };
});