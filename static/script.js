document.addEventListener("DOMContentLoaded", () => {
    let iframe = document.querySelector("iframe");
    let form_input = document.querySelector(".input_box");
    let loader = document.querySelector(".lds-ring");
    let go_back_btn = document.querySelector(".go_back_btn");
    iframe.style.visibility = 'hidden';
    loader.style.visibility = 'hidden';
    go_back_btn.style.visibility = 'hidden';
    go_back_btn.addEventListener("click", () => {
        iframe.style.visibility = 'hidden';
        loader.style.visibility = 'hidden';
        go_back_btn.style.visibility = 'hidden';
        form_input.style.visibility = 'visible';
    });
    document.querySelector(".view_map_btn").addEventListener("click", () => {
        loader.style.visibility = 'visible';
        form_input.style.visibility = 'hidden';
        fetch(`/map/${document.querySelector("input").value}`).then(async response => {
            console.log(response);
            if (response.status === 200 && response.statusText === "OK") {
                let frame = iframe.contentWindow;
                frame.document.open();
                frame.document.write(await response.text());
                frame.document.close();
                iframe.style.visibility = 'visible';
                go_back_btn.style.visibility = 'visible';
                loader.style.visibility = 'hidden';
            } else {
                alert(`Error: ${(await response.json())['error']}`);
                form_input.style.visibility = 'visible';
                loader.style.visibility = 'hidden';
            }
        });
    })
});