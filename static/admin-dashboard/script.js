const url_list_table = document.querySelector("#url-list")
const filter_list_table = document.querySelector("#filter-list")

const url_list_limit = 20
let url_current_page = 0

/**
 * render shorten url list
 * @param {number} start 
 * @param {number} limit 
 * @returns {undefined | bool}
 */
async function renderURLList(start, limit) {
    const url_res = await fetch(`/api/admin/urls?start=${start}&limit=${limit}`, {
        credentials: "same-origin"
    })
    const url_out = await url_res.json()
    if (!url_res.ok) {
        alert(url_out.detail)
        return true
    }
    if (url_out.length === 0) {
        return true
    }

    url_list_table.innerHTML = ""
    url_out.forEach(element => {
        const tr = document.createElement("tr")
        const key = document.createElement("td")
        const original_url = document.createElement("td")
        const created_at = document.createElement("td")
        const delete_btn_cell = document.createElement("td")
        const delete_btn = document.createElement("button")
        const link = document.createElement("a")
        key.textContent = element.key
        link.href = element.original_url
        link.textContent = element.original_url.length > 60
            ? element.original_url.substring(0, 60) + "..."
            : element.original_url
        original_url.appendChild(link)
        created_at.textContent = new Date(element.created_at)
        delete_btn.innerText = "Delete"
        delete_btn.dataset.key = element.key
        delete_btn.onclick = event => deleteShortenURL(event.target.dataset.key)
        delete_btn_cell.appendChild(delete_btn)
        tr.appendChild(key)
        tr.appendChild(original_url)
        tr.appendChild(created_at)
        tr.appendChild(delete_btn_cell)
        url_list_table.appendChild(tr)
    });
}

async function prevURLList() {
    if (url_current_page > 0) {
        url_current_page -= url_list_limit
        await renderURLList(url_current_page, url_list_limit)
    }
}

async function nextURLList() {
    url_current_page += url_list_limit
    if (await renderURLList(url_current_page, url_list_limit)) {
        url_current_page -= url_list_limit
    }
}

async function refreshURLList() {
    url_current_page = 0
    renderURLList(url_current_page, url_list_limit)
}

/**
 * @param {string} key 
 */
async function deleteShortenURL(key) {
    const delete_res = await fetch(`/api/admin/urls?key=${key}`, {
        method: "DELETE",
        credentials: "same-origin"
    })
    if (delete_res.ok) {
        await renderURLList(url_current_page, url_list_limit)
    } else {
        const err = await delete_res.json()
        alert(err.detail)
    }
}

const filter_list_limit = 10
let filter_current_page = 0

/**
 * render filter list
 * @param {number} start 
 * @param {number} limit 
 * @returns {undefined | bool}
 */
async function renderFilterList(start, limit) {
    const filter_res = await fetch(`/api/admin/filters?start=${start}&limit=${limit}`, {
        credentials: "same-origin"
    })
    const filter_out = await filter_res.json()
    if (!filter_res.ok) {
        alert(filter_out.detail)
        return true
    }
    if (filter_out.length === 0) {
        return true
    }

    filter_list_table.innerHTML = ""
    filter_out.forEach(element => {
        const tr = document.createElement("tr")
        const filter = document.createElement("td")
        const created_at = document.createElement("td")
        const delete_btn_cell = document.createElement("td")
        const delete_btn = document.createElement("button")
        filter.textContent = element.filter
        created_at.textContent = new Date(element.created_at)
        delete_btn.innerText = "Delete"
        delete_btn.dataset.id = element.id
        delete_btn.onclick = event => deleteFilter(event.target.dataset.id)
        delete_btn_cell.appendChild(delete_btn)
        tr.appendChild(filter)
        tr.appendChild(created_at)
        tr.appendChild(delete_btn_cell)
        filter_list_table.appendChild(tr)
    });
}

async function prevFilterList() {
    if (filter_current_page > 0) {
        filter_current_page -= filter_list_limit
        await renderFilterList(filter_current_page, filter_list_limit)
    }
}

async function nextFilterList() {
    filter_current_page += filter_list_limit
    if (await renderFilterList(filter_current_page, filter_list_limit)) {
        filter_current_page -= filter_list_limit
    }
}

async function addNewFilter() {
    const add_filter_res = await fetch("/api/admin/filters", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url_filter: document.querySelector("#filter-to-add").value
        }),
        credentials: "same-origin"
    })
    const outcome = await add_filter_res.json()
    if (!add_filter_res.ok) {
        alert(outcome.detail)
        return
    }
    renderFilterList(filter_current_page, filter_list_limit)
}

/**
 * @param {string} id
 */
async function deleteFilter(id) {
    const delete_res = await fetch(`/api/admin/filters?id=${id}`, {
        method: "DELETE",
        credentials: "same-origin"
    })
    if (delete_res.ok) {
        await renderFilterList(filter_current_page, filter_list_limit)
    } else {
        const err = await delete_res.json()
        alert(err.detail)
    }
}

async function logout() {
    await fetch("/api/admin/logout", {
        method: "POST",
        credentials: "same-origin"
    })
    location.reload()
}

async function initDashboard() {
    renderURLList(url_current_page, url_list_limit)
    renderFilterList(filter_current_page, filter_list_limit)
}
