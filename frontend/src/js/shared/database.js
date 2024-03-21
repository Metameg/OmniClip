export function retrieveMedia() {
    return new Promise((resolve, reject) => {
        fetch('/retrieve-user-media')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response failed!');
                }
                return response.json();
            })
            .then(data => {
                // Handle the data returned by the server
                console.log(data);
                resolve(data);
            })
            .catch(error => {
                // Handle errors
                reject(error);
            });
    });
}