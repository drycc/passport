export function groupArray(arr, num) {
    let result = [];
    for (let i = 0, len = arr.length; i < len; i += num) {
        result.push(arr.slice(i, i + num));
    }
    return result
}


export function getCookie(name){
    let ret, m;
    if (typeof name === 'string' && name !== '') {
        if ((m = String(document.cookie).match(
            new RegExp('(?:^| )' + name + '(?:(?:=([^;]*))|;|$)')))) {
            ret = m[1] ? decodeURIComponent(m[1]) : ''
        }
    }
    return ret
}