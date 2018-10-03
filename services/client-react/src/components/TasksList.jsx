import React from 'react';
import {TableBody, TableCell, Table, TableHeader, TableRow, HeaderCell} from "@sendgrid/ui-components"

const TasksList = (props) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <HeaderCell>ID</HeaderCell>
          <HeaderCell>Link</HeaderCell>
          <HeaderCell>Creator</HeaderCell>
          <HeaderCell>Due Date</HeaderCell>
        </TableRow>
      </TableHeader>
      <TableBody>
        { props.tasks.map((task) =>{
          return(
            <TableRow key={task.id}>
              <TableCell className="id">{task.id}</TableCell>
              <TableCell className="link">
                <a href={task.link}>{task.link}</a>
              </TableCell>
              <TableCell className="creator">{task.creator}</TableCell>
              <TableCell className="due_date">{task.due_date}</TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>

  )
};

export default TasksList;