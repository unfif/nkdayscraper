module.exports = {
    publicPath: "/dist/",
    devServer: {
        proxy: {
            "/nkdb/": {target: 'https://db.netkeiba.com'},
            "/nkrace/": {target: 'https://race.netkeiba.com'}
        }
    },
    pages: {
        index: {
            entry: 'src/main.js',
            title: 'NKDayRaces'
        }
    }
};