from flask import request

from .mixins import generic_list_view, generic_detail_view
from .models import Session, Analysis, AnalysisRun, AnalysisExport, AnalysisSend
from .utilities import run_scheduled_send, generate_pdf, login_required


@login_required
def analysis_list_view():
    filter_fields = ['app_id']
    return generic_list_view(Analysis, filter_fields)


@login_required
def analysis_detail_view(id):
    return generic_detail_view(Analysis, id)


@login_required
def analysis_run_list_view():
    filter_fields = ['analysis_id']
    return generic_list_view(AnalysisRun, filter_fields)


@login_required
def analysis_run_detail_view(id):
    return generic_detail_view(AnalysisRun, id)


@login_required
def analysis_export_create_view():
    resp = generic_list_view(AnalysisExport)

    with Session() as session:
        entity = session.query(AnalysisExport).filter_by(id=resp['id']).first()

    pdf_info = generate_pdf(entity.run)
    with Session.begin() as session:
        entity.url = pdf_info['Location']

    return resp


@login_required
def analysis_send_create_view(func_compute):
    resp = generic_list_view(AnalysisSend)

    with Session() as session:
        entity = session.query(AnalysisSend).filter_by(id=resp['id']).first()

    if entity.is_active and not entity.is_ran and not entity.schedule:  # send now
        run_scheduled_send(entity, func_compute)

    return resp


@login_required
def analysis_send_detail_view(id):
    return generic_detail_view(AnalysisSend, id)


@login_required
def compute_view(func_compute):
    params = request.get_json()
    analysis = Analysis(
        id=params.get('analysis_id'),
        params=params
    )
    run = analysis.run(func_compute)

    resp = {
        'analysis': analysis.id,
        'analysis-run': run.id
    }

    return resp
