## own-store

The application provides a graphical interface that allows users to explore, install, and manage a variety of applications using Flatpak. It offers a convenient and efficient way to discover and utilize software in the Linux ecosystem, delivering an experience akin to app stores found on other platforms.

### Adding Apps to the Store

In the file located at src/metadata.json, you can list the applications you wish to make available in the Flathub store: https://flathub.org/

For example, let's list the Google Chrome application (https://flathub.org/apps/com.google.Chrome). As evident from the URL, the identifier is given as "com.google.Chrome". Armed with this information, we can proceed with the listing. The metadata.json file follows this structure:

```json
{
    "name": "app-name",
    "exec": "app-id",
    "icon": "/usr/share/own-store/resources/icon-png",
    "repo": "flatpak",
    "category": "category",
    "description": "app-description"
}
```
Once modified, the file will resemble the following:
```json
{
        "name": "Google Chrome",
        "exec": "com.google.Chrome",
        "icon": "/usr/share/own-store/resources/chrome.png",
        "repo": "flatpak",
        "category": "Internet",
        "description": "Chrome is a web browser developed by Google. It's renowned for its speed, performance, and advanced features. Chrome offers a swift and seamless browsing experience, enabling users to access websites, run web apps, and efficiently perform internet searches. Moreover, Chrome boasts robust security features such as safe browsing and phishing protection, ensuring users stay secure while browsing online. Chrome also supports extensions, allowing users to personalize and enhance their browsing experience according to their needs and preferences."
}
```
Following this, just launch the application, and it will be listed.

### Defined Categories

Within the src/metadata.json file, you can locate the "categories" array, where you can add or remove desired categories. It's important to keep the "More Apps" category at the end.



