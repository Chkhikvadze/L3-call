import { useState } from 'react'

import styled from 'styled-components'

import ReplyIcon from '@l3-lib/ui-core/dist/icons/Replay'
import Copy from '@l3-lib/ui-core/dist/icons/Copy'
import Check from '@l3-lib/ui-core/dist/icons/Check'

type MessageActionsProps = {
  onReplyClick?: () => void
  onCopyClick?: () => void
}

const MessageActions = ({ onReplyClick, onCopyClick }: MessageActionsProps) => {
  const [copied, setCopied] = useState(false)

  const handleCopyClick = () => {
    if (onCopyClick) {
      onCopyClick()
      setCopied(true)

      setTimeout(() => {
        setCopied(false)
      }, 2000)
    }
  }

  return (
    <StyledWrapper>
      {onCopyClick && (
        <StyledActionButton onClick={handleCopyClick}>
          {copied ? <StyledCheckIcon size={20} /> : <StyledCopyIcon size={20} />}
        </StyledActionButton>
      )}
      {onReplyClick && (
        <StyledActionButton onClick={onReplyClick}>
          <StyledReplyIcon />
        </StyledActionButton>
      )}
    </StyledWrapper>
  )
}

export default MessageActions

const StyledWrapper = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0 10px;
`
export const StyledActionButton = styled.div`
  opacity: 0.5;
  :hover {
    opacity: 1;
    cursor: pointer;
  }
`

const StyledReplyIcon = styled(ReplyIcon)`
  path {
    fill: ${({ theme }) => theme.body.iconColor};
  }
`

export const StyledCopyIcon = styled(Copy)`
  path {
    fill: ${({ theme }) => theme.body.iconColor};
  }
`
export const StyledCheckIcon = styled(Check)`
  path {
    fill: ${({ theme }) => theme.body.iconColor};
  }
`
