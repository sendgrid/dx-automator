import React from 'react';
import {TableBody, TableCell, Table, TableHeader, TableRow, HeaderCell} from "@sendgrid/ui-components";

const IssuesList = (props) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <HeaderCell>URL</HeaderCell>
        </TableRow>
      </TableHeader>
      <TableBody>
        {props.issues.map((issue) => {
          return (
            <TableRow key={props.id + '-' + issue.url}>
              <TableCell className="url"><a href={issue.url} target="_blank">{issue.url}</a></TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  );
};

export default IssuesList;
