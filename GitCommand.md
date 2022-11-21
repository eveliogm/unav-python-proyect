
# GIT COMAND GUIDE

## Index:

- [Change Branch](#change-branch)
- [Delete Branch](#delete-branch)
- [Hacer una PR](#hacer-una-pr)
- [Deshacer Cambios](#deshacer-cambios)
- [Unstage changes](#unstage-changes)
- [UnCommit changes](#uncommit-changes)

## Change Branch

If the destination branch does not exist, you have to append the “-b” option, otherwise you won’t be able to switch to that branch.
```
$ git checkout <existing_branch>

$ git checkout -b <new_branch>
```
[Index](#index)


## Delete Branch

Si aún así queremos eliminar esa rama, se puede forzar el borrado de la siguiente manera:
```
$ git branch -D nombre-rama
```
En el caso de querer eliminar una rama del repositorio remoto, la sintaxis será la siguiente:
```
$ git push origin :nombre-rama
```
[Index](#index)



## Hacer una PR

Primero traerse los cambios
```
$ git pull
```
Despues crearse una nueva rama:
```
$ git checkout -b ＜new-branch＞
```


Make some changes and:

```
git add .
git commit -m "message"
```

To undo commit: 

```
git reset --soft HEAD~;
```

To push changes 

```
git push -u origin ＜branch-name＞
```

[Index](#index)


## Deshacer Cambios

For all unstaged files in current working directory use:
```
git checkout ＜branch-name＞ .
```
For a specific file use:

```
git checkout ＜branch-name＞ path/to/file/to/revert
```

For `Git 2.23` onwards, one may want to use the more specific
```
git restore .
```

O para un path especifico:
```
git restore path/to/file/to/revert
```
[Index](#index)


## Unstage changes

Quitar los cambios añadidos con add. Staged changes. 
```
$ git rm --cached pathToFile

```
en el caso de querer quitar todos los archivos csv:
```
$ git rm --cached \*.csv
```
[Index](#index)

## UnCommit changes

Deshcacer cambios de un commit. 
```
$ git reset HEAD~1 --soft

```
de donde:

- reset --> undo changes
- HEAD~1 --> ahead of master 1 commit
- --soft --> no delete files

[Index](#index)

<!-- ## Plantilla
[Index](#index) -->
