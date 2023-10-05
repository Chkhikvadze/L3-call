import { useCreateGroupService } from 'services/group/useCreateGroup'

const Groups = () => {
  const [createGroupService] = useCreateGroupService()

  return (
    <>
      <span> this is group page</span>
      <button onClick={() => createGroupService('gg')}>Create Group</button>
    </>
  )
}

export default Groups
