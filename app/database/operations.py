from uuid import UUID

from sqlmodel import Session, select

from app.database.resource import StreamingResource


def create_resource(
    session: Session,
    url: str,
    title: str,
) -> StreamingResource:
    resource = StreamingResource(url=url, title=title)
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource


def get_resource(session: Session, resource_id: UUID) -> StreamingResource:
    return session.get(StreamingResource, resource_id)


def get_all_resources(session: Session) -> list[StreamingResource]:
    statement = select(StreamingResource)
    return session.exec(statement).all()


def update_resource(
    session: Session, resource_id: UUID, url: str = None, title: str = None
) -> StreamingResource:
    resource = get_resource(session, resource_id)
    if resource:
        if url:
            resource.url = url
        if title:
            resource.title = title
        session.commit()
        session.refresh(resource)

    return resource


def delete_resource(session: Session, resource_id: UUID) -> StreamingResource:
    resource = get_resource(session, resource_id)
    if resource:
        session.delete(resource)
        session.commit()
    return resource
