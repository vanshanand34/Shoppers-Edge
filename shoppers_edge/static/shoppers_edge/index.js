var cPrev = -1;

function sortby(c){
    var i, j;
    var rows = document.getElementById('sortable').rows.length;
    var columns = document.getElementById('sortable').rows[0].cells.length;
    let myarray = Array.from({length:rows},()=> Array(columns).fill(0));
    for(i=0;i<rows;i++){
        for(j=0;j<columns;j++){
            myarray[i][j] = document.getElementById('sortable').rows[i].cells[j].innerHTML;
        }
    }
    var th = myarray.shift();
    if (c !== cPrev) { // different column is clicked, so sort by the new column
        myarray.sort(
            function (a, b) {
                if (a[c] === b[c]) {
                    return 0;
                } else {
                    return (a[c] < b[c]) ? -1 : 1;
                }
            }
        );
    } else { // if the same column is clicked then reverse the array
        myarray.reverse();
    }
    cPrev = c;
    myarray.unshift(th);

    for(i=0;i<rows;i++){
        for(j=0;j<columns;j++){
            document.getElementById('sortable').rows[i].cells[j].innerHTML = myarray[i][j];
        }
    }

}

document.addEventListener('DOMContentLoaded',function(){
    document.addEventListener('click',function(){
        var item = document.getElementById('rating');
        item.addEventListener('click',function(){
            if(item.style.background === 'yellow'){
                item.style.background = 'white';
                item.style.color = 'rgb(95, 64, 38)';
            }else {
                item.style.color = 'black';
                item.style.background = 'yellow';
            } 
        })  
        var item2 = document.getElementById('price');
        item2.addEventListener('click',function(){
            if(item2.style.background === 'yellow'){
                item2.style.background = 'white';
                item2.style.color = 'rgb(95, 64, 38)';
            }else {
                item2.style.color = 'black';
                item2.style.background = 'yellow';
            } 
        })  
    });
    var myelements = document.querySelectorAll('.productitem');
    myelements.forEach(function(element){
        element.onclick = function(){
            let myitem = element.dataset.name;
            $.ajax({
                url: 'my_function',
                method: 'GET',
                data: {
                    'item':myitem
                },
                success: function(data) {
                    if(data.redirect_url){
                        window.location.href = data.redirect_url;
                    }else{
                        console.log('NO url found');
                    }
                },
                error: function(error){
                    console.log('Error:',error);
                }
            });
        };
    });
});

