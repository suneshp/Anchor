from flask_restful import Resource, request
from flask import current_app, send_from_directory, after_this_request
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from models.design import DesignModel
from schemas.design import DesignSchema
from models.result import ResultModel
from models.user import UserModel
from schemas.result import ResultSchema
from libs import image_helper
from flask_uploads import UploadNotAllowed
from libs.strings import gettext
import logging
import traceback
import os

logger = logging.getLogger()
design_schema = DesignSchema()
design_list_schema = DesignSchema(many=True)

FOLDER_NAME="all_results"

class SaveResult(Resource):
    @classmethod
    @jwt_required
    def post(cls):


        if "model_id" in request.form:
            id=request.form.get("model_id")
            print('model_id='+id)
            design = DesignModel.find_by_id(id)
            if not design:
                return {"message": gettext("getfile_design_notfound")}, 404
        else:
            file1 = request.files['resultfile1']
            username = UserModel.find_by_id(get_jwt_identity()).username
            name = file1.filename
            if DesignModel.find_by_designname_and_username(name,username):
                return {"message": gettext("design_name_exists")}, 404
            try:
                folder = f"user_{username}"
                image_path = image_helper.save_image(file1, folder=os.path.join(folder))
            except UploadNotAllowed:  # forbidden file type
                return {"message": gettext("unsupported_fileextension")}, 500
            design = DesignModel(name=name,username=username,objname=image_path)
            try:
                design.save_to_db()
            except:
                traceback.print_exc()
                return {"message": gettext("savemodel_failed")}, 500
            return {"message": gettext("savemodel_stored")}, 200
        if design:
            try:
                username = UserModel.find_by_id(get_jwt_identity()).username
                file1 = request.files['resultfile1']
                image_path = image_helper.save_image(file1, folder=os.path.join(FOLDER_NAME))
                result = ResultModel(name=file1.filename,model_id=design.id,objname=image_path,saved_by=username)
                try:
                    result.save_to_db()
                except:
                    traceback.print_exc()
                    return {"message": gettext("saveresult_failed")}, 500

                return {"message": gettext("saveresult_stored")}, 200
            except:
                traceback.print_exc()
                return {"message": gettext("getfile_file_notfound")}, 404

            return {"message": gettext("getfile_file_notfound")}, 404

        return {"message": gettext("getfile_design_notfound")}, 404
