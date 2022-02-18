let timeout_id = -1;

function set_visibility(visibility, ...entries) {
    entries[0].forEach(entry => {
        entry.style.visibility = visibility;
    });
}

function hide(...entries) {
    set_visibility('hidden', entries)
}

function show(...entries) {
    set_visibility('visible', entries)
}

function setError(error) {
    let error_text = document.querySelector("#error_text");
    error_text.innerHTML = error;
    if (timeout_id !== -1) {
        clearTimeout(timeout_id);
        error_text.classList.toggle('error_text2');
    }
    error_text.classList.toggle('error_text2');
    timeout_id = setTimeout(() => {
        error_text.classList.toggle('error_text2');
        timeout_id = -1;
    }, 5000);
}

document.addEventListener("DOMContentLoaded", () => {
    let iframe = document.querySelector("iframe");
    let input_box = document.querySelector(".input_box");
    let loader = document.querySelector(".lds-ring");
    let go_back_btn = document.querySelector(".go_back_btn");

    hide(iframe, loader, go_back_btn);

    go_back_btn.addEventListener("click", () => {
        hide(iframe, loader, go_back_btn);
        show(input_box);
    });

    document.querySelector(".view_map_btn").addEventListener("click", () => {
        if (document.querySelector("#count_input_box").value <= 0) {
            setError("Count should be positive integer");
            return;
        }

        show(loader);
        hide(input_box);

        fetch('/map?' + new URLSearchParams({
                'user': document.querySelector("#user_input_box").value,
                'count': document.querySelector("#count_input_box").value
            })).then(async response => {
            if (response.status === 200 && response.statusText === "OK") {
                let frame = iframe.contentWindow;
                frame.document.open();
                frame.document.write((await response.json())['map']);
                frame.document.close();

                show(iframe, go_back_btn)
                hide(loader)
            } else {
                setError((await response.json())['error'])

                show(input_box);
                hide(loader);
            }
        });
    })
});
