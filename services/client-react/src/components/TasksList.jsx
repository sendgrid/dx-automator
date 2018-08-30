import React from 'react';
import {Card} from "@sendgrid/ui-components"

const TasksList = (props) => {
  return (
    <div className="list">
        <div className="col-8" >
            { props.tasks.map((task) => {
            return(<Card id="tasks-card" key={task.id} body={task.link}/>)
            })}
        </div>
    </div>
  )
};

export default TasksList;