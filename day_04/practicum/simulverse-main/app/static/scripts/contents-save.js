/* global AFRAME */

/**
 * Component that listens to an event, fades out an entity, swaps the texture, and fades it
 * back in.
 */
 AFRAME.registerComponent('contents-save', {
    schema: {
        space_id: {type: 'string', default:"hello"},
    },

    init: function () 
    {
    
        var self = this;
        this.el.addEventListener('click', function (evt) 
        {
            var el1 = document.querySelectorAll('a-link');
            var jdata = new Object();

            for(elem of el1)
            {
                jdata[elem.getAttribute('origin')] = [elem.getAttribute('position'), elem.getAttribute('rotation')];
            }
            
            this.setAttribute('material', 'color', 'green');

            var url = '/space/scene/link/update/' + self.data.space_id;
            console.log(url)
            var xhr = new XMLHttpRequest();
            
            const getCircularReplacer = () => {
                const seen = new WeakSet();
                return (key, value) => 
                {
                    if (typeof value === "object" && value !== null) 
                    {
                        if (seen.has(value)) {
                            return;
                        }
                        seen.add(value);
                    }
                    return value;
                };
            };

            xhr.open('PUT', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json; charset=utf-8'); 
            
            xhr.onreadystatechange = function() 
            { // Call a function when the state changes.
                if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                    console.log(xhr.responseText);
                }
            }
            //console.log(JSON.stringify(jdata, getCircularReplacer()));
            xhr.send(JSON.stringify(jdata, getCircularReplacer())); 
        });
    }
});