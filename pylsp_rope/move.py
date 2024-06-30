import ast
from typing import List, Optional

from rope.contrib import generate
from rope.refactor import (
    extract,
    inline,
    method_object,
    usefunction,
    localtofield,
    importutils,
    introduce_parameter,
    move
)

from pylsp_rope import typing, commands
from pylsp_rope.project import (
    WorkspaceEditFormat,
    get_project,
    get_resource,
    get_resources,
    apply_rope_changeset,
    DEFAULT_WORKSPACE_EDIT_FORMAT,
)
from pylsp_rope.typing import DocumentUri, CodeActionKind, Range
import rope
from pylsp_rope.refactoring import Command

 

class CommandMoveObject(Command):

    name = commands.COMMAND_MOVE
    kind: typing.CodeActionKind = "refactor.move"
    document_uri: DocumentUri 
    global_: bool
    similar: bool
    range: Range
    destination: str
    _project: rope.base.project.Project
    source_document: str
    destination_document: str


    
    def __call__(
        self,
        *,
        workspace_edit_format: List[
            WorkspaceEditFormat
        ] = DEFAULT_WORKSPACE_EDIT_FORMAT,
        ):

        self.perform_action()

    def perform_action(self):


        self._project = self.project
        resource = self._project.get_resource(self.source_document)
        destination_resource = self._project.get_resource(self.destination_document)


        move_actor = move.create_move(project=self._project, resource=resource, offset=self.range)
        
        move_changes = move_actor.get_changes(destination_resource)

        return self._project.do(move_changes)
