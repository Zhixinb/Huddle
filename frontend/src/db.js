// Exporting database instance from firebase

import firebase from 'firebase/app'
import 'firebase/firestore'

// Get a Firestore instance
export const db = firebase
  .initializeApp({ projectId: 'huddle-be934' })
  .firestore()

// Export types that exists in Firestore
// This is not always necessary, but it's used in other examples
const { Timestamp, GeoPoint } = firebase.firestore
export { Timestamp, GeoPoint }

// if using Firebase JS SDK < 5.8.0
db.settings({ timestampsInSnapshots: true })

var dbHelper = {
    getTimestampBin() {
        var timeNow = new Date();
        var date = timeNow.toLocaleString("en-CA", {
            timeZone: "America/New_York"
        }).split(",")[0];
        var hour = timeNow.toLocaleString("en-CA", {
        hour: "2-digit",
        hour12: false,
        timeZone: "America/New_York"
        }) + ":00:00";
        if (hour == "24:00:00") { //Chrome uses 24 instead of 0 for hours
        hour = "00:00:00"
        }

        return {date, hour}
    },
    logMetric(metric) {
        let {date, hour} = this.getTimestampBin()

        db.collection("metric").doc(date + " " + hour + " " +  metric).set({
            counter: firebase.firestore.FieldValue.increment(1),
            metric: metric,
            last_updated_timestamp: Date.now(),
            timestamp_bin: date + " " + hour
        }, {merge: true})
        .catch((error) => {
            console.error("Error writing document: ", error);
        });
    },
    logUserSession(uid, page, elapsedTime) {
        let {date, hour} = this.getTimestampBin()

        db.collection("usersession").doc(date + " " + hour + " " +  page + " " + uid).set({
            uid: uid,
            page: page,
            elapsed_time_total: firebase.firestore.FieldValue.increment(elapsedTime),
            last_updated_timestamp: Date.now(),
            timestamp_bin: date + " " + hour
        }, {merge: true})
        .catch((error) => {
            console.error("Error writing document: ", error);
        });
    }
}

export default dbHelper