export function groupArray(arr, num) {
    let result = [];
    for (let i=0,len=arr.length;i<len;i+=num) {
        result.push(arr.slice(i, i + num));
    }
    return result
}
