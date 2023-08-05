from projects.picasso.redfish.product.python_api.siasearch import SiaSearch

LOCAL_DEBUG_SERVER = "http://172.17.0.1:5000/"
VIEW_SERVER = "https://siasearch-dev.merantix.de"
API_KEY = "<GET FROM FE>"
PASSWORD = ""  # instead of api key
USER = ""  # instead of api key


def main():
    # sia = SiaSearch(LOCAL_DEBUG_SERVER, API_KEY, viewer_server=VIEW_SERVER)
    sia = SiaSearch.login(LOCAL_DEBUG_SERVER, USER, PASSWORD, viewer_server=VIEW_SERVER)
    print(sia)

    cols = sia.columns()
    print(cols)

    query = sia.query("dataset_name = 'nuscenes' AND curved_trajectory = 'LEFT_BEND'")
    results = query.all()
    print(results.sensor_names())

    cam_front = results.frames("camera_00")
    cam_back = results.frames("camera_02")

    print(cam_front)
    print(cam_back)

    seq = results[5]
    print(seq.frames())
    print(seq)

    print(cam_front[0].f_path)
    print(cam_back[0].f_path)


if __name__ == "__main__":
    main()
