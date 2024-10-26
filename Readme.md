### Requirements

In order to run this script you need to have:
- python(3.x) installed
- pip (python package manager)

When both is installed you need to run the following commands:

```bash
pip install watchdog selenium
```
or
```bash
pip install -r requirements.txt
```

- watchdog is needed to monitor the file and react to changes.
- selenium is used to navigate through whatsapp web and select the correct elemnts via the script


Before running the script you need to adjust some variables based on your need:

```python
# pdf should be replaced with the path to the directory where the file exists
directory_to_watch = os.path.join(os.path.dirname(__file__), "pdf")
```

```python
# pdf_file is the name of the file that shoudl be watched
pdf_file = "sample.pdf"
```

```python
# the name of the whatsapp group the send file should get send to 
whatsapp_group_name = "test123456"
```

On the first run you need authorize the browser and scan the qr-code
