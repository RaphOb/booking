"""
This util and supports  the REST (Read,ReadAll, Update, Delete)
actions for a given model
"""
import logging
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


def read_all(*, model, db_session):
    """
    This function responds to a request for a model
    with the complete list of records
    :return:    json list of all records
    """
    logger.info("Query all model: {}".format(model))
    records = db_session.query(model).all()
    return records


def read_one(*, model, record_id, db_session):
    """
    This function responds to a request for a model
    with one matching record
    :param db_session:
    :param model:
    :param record_id:   Id of record to find
    :return:            record matching id
    """
    logger.info("Query one model: {}".format(model))
    # Query the database for the record
    record = db_session.query(model).filter(model.id == record_id).one_or_none()

    # Was a record found?
    if record is not None:
        logger.warning("Query result not found for id: {}".format(record_id))
        return record

    # Otherwise, nope, didn't find that record
    else:
        None


def update(*, model, record_id, record, db_session):
    """
    This function updates an existing record
    :param db_session:
    :param db:
    :param model:
    :param record_id:   Id of the record to update
    :param record:      record to update
    :return:            updated record, 404 if not found
    """

    logger.info("Query update model: {}".format(model))
    # Get the record requested from the db into session
    update_record = db_session.query(model).filter(model.id == record_id).one_or_none()

    if update_record is not None:
        logger.info("Result found, processing update")
        model_data = jsonable_encoder(update_record)
        update_data = record.dict(exclude_unset=True)
        for field in model_data:
            if field in update_data:
                setattr(update_record, field, update_data[field])

        # merge the new object into the old and commit it to the db
        db_session.add(update_record)
        db_session.commit()

        # return updated record in the response

        return update_record

    # Otherwise, nope, didn't find that record
    return None


def delete(*, model, record_id, db_session):
    """
    This function deletes a record
    :param db_session:
    :param db:
    :param model:
    :param record_id:   Id of the record to delete
    :return:            204 on successful delete, 404 if not found
    """
    logger.info("Query delete for model: {}".format(model))
    # Get the record requested
    record = db_session.query(model).filter(model.id == record_id).one_or_none()

    # Did we find a record?
    if record is not None:
        logger.info("Result found processing delete")
        db_session.delete(record)
        db_session.commit()
        return "", 204

    # Otherwise, nope, didn't find that record
    return None
