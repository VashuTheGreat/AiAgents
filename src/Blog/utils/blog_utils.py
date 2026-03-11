import re
import os
import logging

def delete_blog_content(data: dict):
    """
    Deletes the blog markdown file and its associated images.
    :param data: The blog data dictionary containing 'plan', 'final', and 'topic'.
    :return: True if the blog was successfully deleted, False otherwise.
    """
    try:
        # 1. Identify the blog file
        plan = data.get("plan")
        blog_title = None
        
        # 'plan' might be a dictionary or a custom object
        if isinstance(plan, dict):
            blog_title = plan.get("blog_title")
        elif hasattr(plan, "blog_title"):
            blog_title = plan.blog_title
        
        if not blog_title:
            blog_title = data.get("topic")
        
        if not blog_title:
            logging.error("Could not find blog title in data")
            return False

        md_filename = f"{blog_title}.md"
        md_file_path = os.path.join("results", md_filename)

        # 2. Find images referenced in final markdown
        final_md = data.get("final", "")
        if not final_md:
            # If final md is not in data, try reading it from file
            if os.path.exists(md_file_path):
                try:
                    with open(md_file_path, "r", encoding="utf-8") as f:
                        final_md = f.read()
                except Exception as e:
                    logging.warning(f"Could not read blog file: {str(e)}")

        # Regex to find image paths like ../images/filename.png
        # Format: ![alt](../images/filename.png)
        image_pattern = r"!\[.*?\]\(\.\./images/(.*?)\)"
        image_filenames = re.findall(image_pattern, final_md)

        # 3. Delete images
        for img_name in image_filenames:
            img_path = os.path.join("images", img_name)
            if os.path.exists(img_path):
                logging.info(f"Deleting image: {img_path}")
                try:
                    os.remove(img_path)
                except Exception as e:
                    logging.error(f"Failed to delete image {img_path}: {str(e)}")
            else:
                logging.warning(f"Image not found: {img_path}")

        # 4. Delete markdown file
        if os.path.exists(md_file_path):
            logging.info(f"Deleting blog: {md_file_path}")
            try:
                os.remove(md_file_path)
                return True
            except Exception as e:
                logging.error(f"Failed to delete blog file {md_file_path}: {str(e)}")
                return False
        else:
            logging.warning(f"Blog file not found: {md_file_path}")
            return False

    except Exception as e:
        logging.error(f"Error in delete_blog_content: {str(e)}")
        return False
