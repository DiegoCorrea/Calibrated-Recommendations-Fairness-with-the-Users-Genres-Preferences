def download():
    import gdown
    output = 'dataset.zip'
    # url = 'https://drive.google.com/uc?id=1mc7ZsI5HEeLwbDRJ3f8JHUWl2tjlljKh'
    # url = 'https://drive.google.com/uc?id=1-VRVh2T_8UeZzQat3g1zVO0gwAhO6lRW'
    url = 'https://drive.google.com/uc?id=1bjLEZLhkK-hB4g3Ploz4iAMpN2jGKm7A'

    gdown.download(url, output, quiet=False)


if __name__ == '__main__':
    download()
