from pathlib import Path
from typing import Dict, List
from nubia import command, argument, context
from rich.console import Console
from rich.table import Table
from rich import inspect, print

import System
from Microsoft.Diagnostics.Runtime import ClrElementType
from ..context import TurdshovelContext


@command
@argument("filter_", type=str, name="filter", description="Filter objects by string")
def dumpheap(filter_: str = ".") -> None:
    """Dumps the objects on the heap"""
    ctx: TurdshovelContext = context.get_context()
    runtime = ctx.runtime
    console: Console = ctx.console

    # TODO: Turn this into a decorator for reuse
    if not ctx.runtime:
        console.print("[bold red] No runtime loaded! Load a dump first!")
        return

    if not runtime.Heap.CanWalkHeap:
        console.print("[bold red]ERROR: Cannot walk heap![/]")
        return

    object_table = Table(border_style="#8B4513")
    object_table.add_column("Address", style="cyan")
    object_table.add_column("Size", style="green")
    object_table.add_column("Object", style="yellow", overflow="fold")

    for segment in runtime.Heap.Segments:
        for obj in segment.EnumerateObjects():
            if obj.IsValid and not obj.IsFree:
                if filter_.lower() in obj.ToString().lower():
                    object_table.add_row(
                        hex(obj.Address), str(obj.Size), obj.ToString().split()[0]
                    )
    console.print(object_table, highlight=True)


def _iter_field(runtime, obj, field, top_level=True):
    """Recursively iterates through fields"""
    inspect(field, all=True)

    element_type = field.get_ElementType()

    if element_type == ClrElementType.String:
        field_data = obj.ReadStringField(field.Name)

    elif element_type == ClrElementType.Boolean:
        field_data = obj.ReadField[bool](field.Name)

    elif element_type == ClrElementType.Int8:
        field_data = obj.ReadField[System.Int8](field.Name)
    elif element_type == ClrElementType.Int16:
        field_data = obj.ReadField[System.Int16](field.Name)
    elif element_type == ClrElementType.Int32:
        field_data = obj.ReadField[System.Int32](field.Name)
    elif element_type == ClrElementType.Int32:
        field_data = obj.ReadField[System.Int64](field.Name)
    elif element_type == ClrElementType.UInt8:
        field_data = obj.ReadField[System.Byte](field.Name)
    elif element_type == ClrElementType.UInt16:
        field_data = obj.ReadField[System.UInt16](field.Name)
    elif element_type == ClrElementType.UInt32:
        field_data = obj.ReadField[System.UInt32](field.Name)
    elif element_type == ClrElementType.UInt64:
        field_data = obj.ReadField[System.UInt64](field.Name)
    elif element_type == ClrElementType.Float:
        field_data = obj.ReadField[System.Single](field.Name)
    elif element_type == ClrElementType.Double:
        field_data = obj.ReadField[System.Double](field.Name)

    elif element_type in [ClrElementType.Class, ClrElementType.Object]:
        field_data = {}
        sub_obj = runtime.Heap.GetObject(obj.ReadObjectField(field.Name).Address)
        if sub_obj.IsValid and not sub_obj.IsFree:
            if sub_obj.Type:
                for sub_field in sub_obj.Type.Fields:
                    field_data[sub_field.Name] = _iter_field(
                        runtime, sub_obj, sub_field, False
                    )
            else:
                inspect(sub_obj, all=True)
        elif sub_obj.IsNull:
            field_data = None

    elif element_type == ClrElementType.SZArray:
        field_data = "No"

        # array_object = obj.ReadObjectField(field.Name)
        # if array_object.Type and array_object.Type.Name.startswith(
        #     "System.Collections.Generic.Dictionary"
        # ):
        #     print("DICT!")
        # field_data = None if array_object.IsNull else array_object.AsArray()
    elif field.IsValueType:
        field_data = {}
        value_obj = obj.ReadValueTypeField(field.Name)
        for sub_field in value_obj.get_Type().Fields:
            field_data[sub_field.Name] = _iter_field(
                runtime, value_obj, sub_field, False
            )
        # sub_obj = runtime.Heap.GetObject(value_obj.Address)
        # inspect(value_obj, title=field.Name)
        # inspect(value_obj.get_Type())
        # inspect(sub_obj)
    else:
        inspect(field, all=True)

    return field_data


@command
@argument(
    "address",
    type=str,
    positional=True,
    description="Address of object to dump. Hex format (0x12345678)",
)
def dumpobj(address: str) -> None:
    """Dumps an object on the heap by address"""
    ctx: TurdshovelContext = context.get_context()
    runtime = ctx.runtime
    console: Console = ctx.console

    # TODO: Turn this into a decorator for reuse
    if not ctx.runtime:
        console.print("[bold red] No runtime loaded! Load a dump first!")
        return

    if not runtime.Heap.CanWalkHeap:
        console.print("[bold red]ERROR: Cannot walk heap![/]")
        return

    address = int(address, 16)
    obj = runtime.Heap.GetObject(address)

    if obj.IsValid and not obj.IsFree:

        output = {}
        try:
            for field in obj.Type.Fields:
                output[field.Name] = _iter_field(runtime, obj, field)
            print(output)
        except RecursionError:
            console.print_exception(show_locals=True)
            console.print(
                "Recursion error happened. Logic needs to be fixed to handle this type"
            )
        except Exception:
            console.print_exception()

    # console.print(object_table, highlight=True)
