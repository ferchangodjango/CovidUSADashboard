
//fetch('https://api.finazon.io/latest/datasets?page_size=1000&apikey=9bb3dddf5e0748ad9e8be8b9fa670dd8vm')
fetch('https://api.finazon.io/latest/datasets=crypto&time_series?ticker=BTC%2FUSDT&interval=1d&page=0&page_size=30&apikey=9bb3dddf5e0748ad9e8be8b9fa670dd8vm')
    .then((resp)=>resp.json())
    .then((resp)=>console.log(resp));