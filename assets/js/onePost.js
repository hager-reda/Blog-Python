
/*<script type="text/javascript">*/
    console.log( `{{urlike}}` )
    sendReply()
    sendComment()
    addLike()

    function sendReply()
    {
        {% for comment in comments %}
            repBtn{{comment.id}} = document.querySelector('#repBtn{{comment.id}}')
            reptextarea{{comment.id}} = document.querySelector('#reptextarea{{comment.id}}')
            repcount{{comment.id}} = document.querySelector('#repcount{{comment.id}}')

            add{{comment.id}} = document.querySelector('.appendRep{{comment.id}}').lastElementChild
            append{{comment.id}} = document.querySelector('.appendRep{{comment.id}}')
            add{{comment.id}}.style.display="none"


            repBtn{{comment.id}}.addEventListener('click', (ev) => 
            {
                ev.preventDefault()
                console.log("reply")
                console.log(reptextarea{{comment.id}}.value)
                url = "/posts/reply/?post={{post.id}}&comment={{comment.id}}&text=" + reptextarea{{comment.id}}.value
                console.log(url)

                add{{comment.id}} = document.querySelector('.appendRep{{comment.id}}').lastElementChild

                let xhr = new XMLHttpRequest();
                xhr.open("GET", url)
                xhr.send();

                xhr.onload = () => {
                    console.log('onload');
                    console.log(xhr.status);
                    if (xhr.status === 200) 
                    {
                        console.log(typeof (xhr.response));
                        const json = JSON.parse(xhr.response);
                        console.log(json)

                        reptextarea{{comment.id}}.value=""
                        repcount{{comment.id}}.textContent = json.count+"Replys"

                        let addEl = document.createElement("div")
                        addEl.setAttribute('class', "card card-body")
                        append{{comment.id}}.appendChild(addEl)

                        let addid = document.createElement("div")
                        addid.setAttribute('class', "commentid")
                        addEl.appendChild(addid)

                        let addtxt = document.createElement("div")
                        addtxt.setAttribute('class', "commenttext")
                        addEl.appendChild(addtxt)

                        let addtm = document.createElement("div")
                        addtm.setAttribute('class', "commenttime")
                        addEl.appendChild(addtm)

                        addEl.style.display="none"
                        add{{comment.id}}.style.display="block"

                        add{{comment.id}}.querySelector(".replyid").textContent="{{request.user}}"
                        add{{comment.id}}.querySelector(".replytext").textContent=json['newReply']
                        add{{comment.id}}.querySelector(".replytime").textContent='Now..'
                    } 
                    else 
                    {
                        console.log(xhr.status);
                    }
                }
            });
        {% endfor %}
    }


    function sendComment()
    {
    commentBtn = document.querySelector('#commentBtn')
    textarea = document.querySelector('#textarea')
    count = document.querySelector('#count')
    add = document.querySelector('.append').lastElementChild
    append = document.querySelector('.append')
    add.style.display="none"

        commentBtn.addEventListener('click', (ev) => 
        {
            ev.preventDefault()
            console.log(`{{post.id}}`)
            url = "/posts/comment/?post=" + `{{post.id}}`+"&text=" + textarea.value
            // sendComment(url)

            let xhr = new XMLHttpRequest();
            xhr.open("GET", url)
            xhr.send();

            xhr.onload = () => {
                console.log('onload');
                console.log(xhr.status);
                if (xhr.status === 200) 
                {
                    console.log(typeof (xhr.response));
                    const json = JSON.parse(xhr.response);
                    console.log(json)

                    textarea.value=""
                    count.textContent = json.count+"Comments"

                    let addEl = document.createElement("div")
                    addEl.setAttribute('class', "card card-body")
                    append.appendChild(addEl)

                    let addid = document.createElement("div")
                    addid.setAttribute('class', "commentid")
                    addEl.appendChild(addid)

                    let addtxt = document.createElement("div")
                    addtxt.setAttribute('class', "commenttext")
                    addEl.appendChild(addtxt)

                    let addtm = document.createElement("div")
                    addtm.setAttribute('class', "commenttime")
                    addEl.appendChild(addtm)

                    addEl.style.display="none"
                    add.style.display="block"

                    add.querySelector(".commentid").textContent=`{{request.user}}`
                    add.querySelector(".commenttext").textContent=json['newComment']
                    add.querySelector(".commenttime").textContent='Now..'
                } 
                else 
                {
                    console.log(xhr.status);
                }
            }

        });
    }

    function addLike()
    {
        console.log( `{{urlike}}` )
        showImg = document.querySelector("#showImg")
        showlike = document.querySelector("#showlike")
        showdislike = document.querySelector("#showdislike")
        none = document.querySelector("#none")
        alike = document.querySelector("#dolike")

                showImg.style.display="none"

            act="none"

            if ( `{{urlike}}` == 'like') 
            {
                like.style.color="blue"
                dislike.style.color="black"
                act="like"
            }
            else if ( `{{urlike}}` == 'dislike' ) 
            {
                like.style.color="black"
                dislike.style.color="red"
                act="dislike"
            }
            else
            {
                like.style.color="black"
                dislike.style.color="black"
                act="none"
            }

        showlike.addEventListener('mouseover',(ev)=>{
            console.log(ev)
            ev.preventDefault()
            showlike.style.width='50px'
            showlike.style.height='50px'
        });
        showlike.addEventListener('mouseout',(ev)=>{
            console.log(ev)
            ev.preventDefault()
            showlike.style.width='30px'
            showlike.style.height='30px'
        });
        showlike.addEventListener('click',(ev)=>{
            console.log(ev)
            ev.preventDefault()
            showlike.style.width='50px'
            showlike.style.height='50px'
            act = "like"
            like.style.color="blue"
            dislike.style.color="black"
            url = "/posts/like/?post={{post.id}}&like="+act
            sendLike(url)
        });
        showdislike.addEventListener('mouseover',(ev)=>{
            console.log(ev)
            ev.preventDefault()
            showdislike.style.width='50px'
            showdislike.style.height='50px'
        });
        showdislike.addEventListener('mouseout',(ev)=>{
            console.log(ev)
            ev.preventDefault()
            showdislike.style.width='30px'
            showdislike.style.height='30px'
        });
        showdislike.addEventListener('click',(ev)=>{
            console.log(ev)
            ev.preventDefault()
            showdislike.style.width='50px'
            showdislike.style.height='50px'
            act = "dislike"
            like.style.color="black"
            dislike.style.color="red"
            url = "/posts/like/?post={{post.id}}&like="+act
            sendLike(url)
        });

        alike.addEventListener('mouseover',(ev)=>{
            console.log(ev)
            ev.preventDefault()
                showImg.style.display="block"
        });

        alike.addEventListener('mouseout',(ev)=>{
            console.log(ev)
            ev.preventDefault()
                showImg.style.display="none"
        });

        none.addEventListener('click',(ev)=>{
            console.log(ev)
            ev.preventDefault()
            act="none"
            like.style.color="black"
            dislike.style.color="black"
            url = "/posts/like/?post={{post.id}}&like="+act
            sendLike(url)
        });

    }

    function sendLike(url)
    {
        like = document.querySelector("#like")
        dislike = document.querySelector("#dislike")

        let xhr = new XMLHttpRequest();
            xhr.open("GET", url)
            xhr.send();

            xhr.onload = () => {
                console.log('onload');
                console.log(xhr.status);
                if (xhr.status === 200) 
                {
                    console.log(typeof (xhr.response));
                    const json = JSON.parse(xhr.response);
                    console.log(json)

                    console.log('done');
                    like.textContent = json.countlike+"likes" 
                    dislike.textContent = json.countdislike+"dislikes"
                } 
                else 
                {
                    console.log(xhr.status);
                }
            }
    }



/*</script>*/