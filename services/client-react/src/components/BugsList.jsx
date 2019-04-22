import React from 'react';
import {TableBody, TableCell, Table, TableHeader, TableRow, HeaderCell} from "@sendgrid/ui-components"

const BugsList = (props) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <HeaderCell>URL</HeaderCell>
        </TableRow>
      </TableHeader>
      <TableBody>
        { props.bugs.map((bug) =>{
          return(
            <TableRow>
              <TableCell className="url"><a href={bug.url}>{bug.url}</a></TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>

  )
};

export default BugsList;