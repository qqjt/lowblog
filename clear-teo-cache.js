// Tencent cloud EdgeOne 'CreatePurgeTask' api: https://cloud.tencent.com/document/api/1552/80703

const tencentCloud = require("tencentcloud-sdk-nodejs-teo");
const TeoClient = tencentCloud.teo.v20220901.Client

const args = process.argv.slice(2);
console.log("Arguments:", args);

let baseUrl = process.env.BASE_URL;
const secretId = process.env.TENCENTCLOUD_SECRET_ID
const secretKey = process.env.TENCENTCLOUD_SECRET_KEY
const zoneId = process.env.TENCENTCLOUD_TEO_ZONE_ID

if (baseUrl) {
  if (!baseUrl.endsWith('/')) {
    baseUrl = `${baseUrl}/`;
  }
}

if (!baseUrl || !secretId || !secretKey || !zoneId) {
  console.warn('not enough env variables')
  process.exit()
}

/**
 * call CreatePurgeTask api
 * @param urlList
 */
const clearTeoCache = (urlList) => {
  const client = new TeoClient({
    credential: {
      secretId: secretId,
      secretKey: secretKey,
    }
  })
  const data = {
    "Targets": urlList,
    "Type": "purge_url",
    "ZoneId": zoneId
  }
  client.CreatePurgeTask(data).then(
    (data) => {
      console.log(data)
    },
    (err) => {
      console.error("error", err)
    }
  )
}

/**
 * build url from file
 * @param filePath
 * @returns {string}
 */
const filePathUri = (filePath) => {
  const pathParts = filePath.split("/");
  if (pathParts.length > 1) {
    if (pathParts[0] === 'source' && pathParts[1] === '_posts') {
      const fileName = pathParts[pathParts.length - 1];
      if (fileName.endsWith(".md")) {
        const urlParts = pathParts.slice(2, pathParts.length - 1);
        const fileNameUri = fileName.substring(0, fileName.lastIndexOf(".md"));
        urlParts.push(fileNameUri)
        return urlParts.join("/") + '/';
      }
    }
  }
  return ''
}

const main = () => {
  let clearList = []
  for (let filePath of args) {
    const uri = filePathUri(filePath)
    if (uri) {
      clearList.push(`${baseUrl}${uri}`);
    }
  }
  if (clearList.length) {
    clearList.push(`${baseUrl}archives/`)
  }
  console.log(clearList);
  if (clearList.length) {
    clearTeoCache(clearList)
  }
}
main()