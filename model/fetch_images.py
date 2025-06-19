from icrawler.builtin import BingImageCrawler
import os
import glob
import shutil

def fetch_station_images(query, out_dir, max_num=20):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    crawler = BingImageCrawler(storage={"root_dir": out_dir})
    crawler.crawl(keyword=query, max_num=max_num)

def rename_and_flatten(temp_base_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    all_images = glob.glob(os.path.join(temp_base_dir, "**", "*.*"), recursive=True)
    index = 1
    for filepath in all_images:
        if filepath.lower().endswith((".jpg", ".jpeg", ".png")):
            ext = os.path.splitext(filepath)[1]
            shutil.move(filepath, os.path.join(target_dir, f"{index}{ext}"))
            index += 1

    shutil.rmtree(temp_base_dir, ignore_errors=True)

if __name__ == "__main__":
    queries = [
        "Hannover Kröpcke tram stop",
        "Hamburg Dammtor station",
        "Berlin Hauptbahnhof entrance",
        "Berlin Alexanderplatz station",
        "Munich Marienplatz station",
        "Frankfurt am Main Hauptbahnhof",
        "bus stop in rural area",
        "rural train station Germany",
        "old tram stop without accessibility",
        "wheelchair accessible bus stop",
        "tram station tactile paving",
        "train station elevator",
        "ramp to train platform",
        "accessible bus stop entrance",
        "train station with tactile guidance system",
        "blind friendly station design",
        "station wheelchair ramp",
        "not accessible bus stop",
        "train station stairs only",
        "bus stop without ramp",
        "station with broken elevator",
        "narrow platform train station",
        "covered vs uncovered bus stop",
        "night photo of tram station",
        "crowded train platform",
        "tram station entrance"
    ]

    temp_dir = "temp_download"
    final_dir = "training_images"

    for query in queries:
        subfolder = os.path.join(temp_dir, query.replace(" ", "_"))
        print(f"Fetching: {query}")
        fetch_station_images(query, subfolder, max_num=20)

    print("🔁 Download abgeschlossen. Bilder werden jetzt zusammengeführt …")
    rename_and_flatten(temp_dir, final_dir)
    print("✅ Fertig! Alle Bilder befinden sich durchnummeriert in 'training_images/'")
